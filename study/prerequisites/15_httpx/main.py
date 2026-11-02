"""httpx 예제 — 커넥션 풀, 타임아웃, 재시도, 스트리밍, SSRF 프록시.

Dify 에서의 용도
  - 외부 HTTP 호출은 대부분 httpx 로 한다.
    (HTTP Request 노드, 툴, 웹 크롤링, 원격 파일 다운로드, 플러그인 데몬 통신 ...)
  - api/core/helper/ssrf_proxy.py  ← 사용자 입력 URL 을 호출할 때 반드시 거치는 래퍼
      * 모든 요청을 Squid SSRF 프록시(docker 의 ssrf_proxy 컨테이너, :3128) 경유
        → 사설망/루프백/메타데이터 주소(169.254.169.254 등) 접근을 프록시가 403 으로 차단
      * 403 응답의 Server/Via 헤더에 squid 가 있으면 ToolSSRFError 로 변환
      * 429/5xx 에 대해 지수 백오프 재시도 (BACKOFF_FACTOR * 2**n)
      * 세분화된 Timeout(connect/read/write), Limits(max_connections ...) 로 풀링된 Client 재사용
  - api/core/helper/http_client_pooling.py : 키별로 httpx.Client 를 캐싱해 커넥션 재사용

이 예제는 대부분 httpx.MockTransport(가짜 서버)로 네트워크 없이 동작한다.
마지막 단계는 로컬 dev middleware 의 ssrf_proxy(localhost:3128) 가 떠 있으면 실제로 차단을 보여준다.
실행: uv run --project api python example/15_httpx/main.py
"""

import json
import os
import time
import httpx

BACKOFF_FACTOR = 0.1
STATUS_FORCELIST = [429, 500, 502, 503, 504]

class ToolSSRFError(Exception): ...

_flasky_counter = {"n": 0}

def custom_handler(request: httpx.Request) -> httpx.Response:
   match request.url.path:
      case "/json":
         return httpx.Response(200, json={"hello": "dify", "ua": request.headers["user-agent"]})
      case "/flaky":
         _flasky_counter["n"] += 1
         if _flasky_counter["n"] < 3:
            return httpx.Response(503, text="service unavailable")
         return httpx.Response(200, text=f"ok after {_flasky_counter['n']} attempts")
      case "/slow":
         raise httpx.ReadTimeout("read timed out", request=request)
      case "/stream":
         return httpx.Response(200, content=iter([b"chunk-1", b"chunk-2", b"chunk-3"]))
      case _:
         return httpx.Response(404)

def make_request(client: httpx.Client, method: str, url: str, max_retries: int = 3, **kwargs) -> httpx.Response:
    retries = 0
    while retries <= max_retries:
      try:
         response = client.request(method, url, **kwargs)
         if (
            response.status_code in (401, 403)
            and "squid" in (response.headers.get("server", "") + response.headers.get("via", "")).lower()
         ):
            raise ToolSSRFError(f"Access to '{url}' was blocked by SSRF protection")
         if response.status_code not in STATUS_FORCELIST:
            return response
         print(f"   attempt {retries + 1}: status {response.status_code}")
      except httpx.RequestError as e:
         print(f"   attempt {retries + 1}: {type(e).__name__} → retry")

      retries += 1
      if retries <= max_retries:
         time.sleep(BACKOFF_FACTOR * (2 ** (retries - 1)))
    raise RuntimeError(f"Reached maximum retries ({max_retries}) for URL {url}")




def main() -> None:
  client = httpx.Client(
     transport=httpx.MockTransport(custom_handler),
     base_url="http://cloud.local",
     headers={"User-Agent": "Dify-Example/1.0"},
     timeout=httpx.Timeout(10.0, connect=2.0, read=5.0, write=5.0),
  )

  print("1. Json 기본 요청")
  r = client.get("/json", params={"q": "test"})
  print("  ", r.status_code, r.request.url, r.json())

  print("\n2. 5xx 재시도 + 지수 백오프")
  r = make_request(client, "GET", "/flaky")
  print("  ", r.status_code, r.text)

  print("\n3. 타임아웃 -> 재시도 후 실패")
  try:
     make_request(client, "GET", "/slow", max_retries=2)
  except RuntimeError as e:
    print("  ", e)

  print("\n4. 스트리밍 다운로드 (대용량 파일을 메모리에 다 올리지 않기)")
  with client.stream("GET", "/stream") as r:
     for chunk in r.iter_bytes():
        print("   received:", chunk)

  print("\n5. 이벤트 훅 (요청/응답 로깅)")
  hooked = httpx.Client(
     transport=httpx.MockTransport(custom_handler),
     base_url="http://cloud.local",
     event_hooks={
        "request": [lambda req: print(f"   → {req.method} {req.url}")],
        "response": [lambda res: print(f"   ← {res.status_code} {res.request.url.path}")],
     },
  )
  hooked.post("/json", content=json.dumps({"a": 1}))

  print("\n5. SSRF 프록시 경유 (localhost:3128 의 Squid)")
  proxy_url = os.getenv("SSRF_PROXY_ALL_URL", "http://localhost:3128")
  ssrf_client = httpx.Client(proxy=proxy_url, timeout=5)
  try:
     ssrf_client.get("http://example.com", timeout=2)
  except httpx.ProxyError:
     print(
        f"   ssrf_proxy({proxy_url}) 가 떠 있지 않아 생략"
     )
     return
  except httpx.RequestError:
     ...

  for url in ["http://127.0.0.1:5001/console/api/setup", "http://169.254.169.254/latest/meta-data/"]:
     try:
        r = make_request(ssrf_client, "GET", url, max_retries=0)
        print(f"   {url} → {r.status_code}")
     except ToolSSRFError as e:
        print(f"   차단됨: {e}")


if __name__ == "__main__":
    main()
