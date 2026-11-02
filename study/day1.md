## docker compose up -d

- 파일경로: docker/docker-compose.yaml
- 핵심클래스/함수: .env
- 역할:
- 의문점:
- docker/.env.example이 현행화가 안되어 있어서 DIFY_AGENT_LOCAL_SANDBOX_AUTH_TOKEN 속성 및 추가된 속성이 었어서 sandbox, dify-agent container가 ready상태가 안되었다.

  > local_sandbox-1 | shellctl: auth token is required: set SHELLCTL_AUTH_TOKEN or --token

- openssl rand -hex 32로 토큰을 만들어서 설정하면 된다.
- docker compose config로 설정값을 조회할 수 있다.

## api debug 방법

- repo root에 .vscode/launch.json.template 파일을 복사하여 launch.json 로 생성하면 vscode debug 화면에서 Python: API를 디버깅할 수 있다.
- api/.vscode 하위에도 launch.json.template 파일이 있는데 이 용도는 무엇일까?
