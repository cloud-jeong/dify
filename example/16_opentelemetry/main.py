"""OpenTelemetry 예제 — 분산 트레이싱 (자동 계측 + 수동 span).

Dify 에서의 용도 (ENABLE_OTEL=true 일 때)
  - api/extensions/ext_otel.py
      TracerProvider(resource=Resource(service.name=...)), Sampler(OTEL_SAMPLING_RATE)
      BatchSpanProcessor(OTLPSpanExporter)  → Jaeger / Tempo / Grafana / 클라우드 APM 으로 전송
  - api/extensions/otel/instrumentation.py
      FlaskInstrumentor, SQLAlchemyInstrumentor, RedisInstrumentor, HTTPXClientInstrumentor, CeleryInstrumentor
      → 코드 수정 없이 HTTP 요청, SQL, Redis 명령, 외부 HTTP 호출, Celery 태스크가 span 으로 기록됨
  - api/extensions/otel/decorators/ : 비즈니스 로직(워크플로/노드 실행 등)에 수동 span 을 다는 데코레이터
  - api/app_factory.py : 응답 헤더에 X-Trace-Id 를 붙여 사용자 문의 시 트레이스 추적 가능
  ※ LLM 호출 단위의 "앱 트레이싱"(Langfuse, LangSmith 등)은 별개 기능: api/providers/trace/*

이 예제는 콘솔 exporter 로 span 트리를 출력한다. (OTLP 대신)
실행: uv run --project api python example/16_opentelemetry/main.py
"""

import time
from collections import defaultdict

import httpx
from flask import Flask, jsonify
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter, SpanExportResult
from sqlalchemy import create_engine, text


class TreeExporter(SpanExporter):
    """span 을 모아두었다가 부모-자식 트리로 출력 (ConsoleSpanExporter 는 JSON 이 너무 길어서)."""

    def __init__(self) -> None:
        self.spans: list[ReadableSpan] = []

    def export(self, spans):
        self.spans.extend(spans)
        return SpanExportResult.SUCCESS

    def print_tree(self) -> None:
        children = defaultdict(list)
        for s in self.spans:
            children[s.parent.span_id if s.parent else None].append(s)

        def walk(parent_id, depth):
            for s in sorted(children[parent_id], key=lambda x: x.start_time):
                ms = (s.end_time - s.start_time) / 1e6
                attrs = {
                    k: v
                    for k, v in s.attributes.items()
                    if k
                    in ("http.route", "http.status_code", "db.statement", "workflow.node_id", "http.url", "url.full")
                }
                print(f"{'  ' * depth}- {s.name:<34} {ms:7.2f}ms  {attrs}")
                walk(s.context.span_id, depth + 1)

        walk(None, 0)


# ---------------------------------------------------------------------------
# 1) Provider 설정 (ext_otel.py)
# ---------------------------------------------------------------------------
exporter = TreeExporter()
provider = TracerProvider(
    resource=Resource.create({"service.name": "dify-api-example", "deployment.environment": "dev"})
)
provider.add_span_processor(SimpleSpanProcessor(exporter))  # Dify: BatchSpanProcessor(OTLPSpanExporter(...))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("example.workflow")

# ---------------------------------------------------------------------------
# 2) 앱 + 자동 계측
# ---------------------------------------------------------------------------
app = Flask(__name__)
engine = create_engine("sqlite:///:memory:")
FlaskInstrumentor().instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)

# 가짜 LLM 서버. (Dify 는 HTTPXClientInstrumentor().instrument() 로 전역 계측하지만,
#  MockTransport 는 전역 계측 대상인 기본 transport 를 우회하므로 여기선 클라이언트 단위로 계측)
upstream = httpx.Client(transport=httpx.MockTransport(lambda req: httpx.Response(200, json={"text": "LLM says hi"})))
HTTPXClientInstrumentor.instrument_client(upstream)


def run_node(node_id: str, fn):
    # 3) 수동 span: 비즈니스 단위(워크플로 노드) 계측 (extensions/otel/decorators 의 역할)
    with tracer.start_as_current_span(f"workflow.node.{node_id}") as span:
        span.set_attribute("workflow.node_id", node_id)
        try:
            return fn()
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR))
            raise


@app.post("/v1/workflows/run")
def run_workflow():
    with engine.connect() as conn:
        conn.execute(text("select 1 /* load workflow */"))
    run_node("start", lambda: time.sleep(0.01))
    llm = run_node("llm", lambda: upstream.post("https://api.llm-provider.example/v1/chat").json())
    run_node("end", lambda: time.sleep(0.005))

    span_ctx = trace.get_current_span().get_span_context()
    resp = jsonify(outputs=llm)
    resp.headers["X-Trace-Id"] = format(span_ctx.trace_id, "032x")  # app_factory.py add_trace_headers
    return resp


def main() -> None:
    r = app.test_client().post("/v1/workflows/run")
    print("response:", r.get_json(), "| X-Trace-Id:", r.headers["X-Trace-Id"])
    print("\n수집된 span 트리 (하나의 trace):")
    exporter.print_tree()
    print("\ntrace_id 모두 동일?", len({s.context.trace_id for s in exporter.spans}) == 1)


if __name__ == "__main__":
    main()
