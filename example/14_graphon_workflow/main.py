"""graphon 워크플로 엔진 최소 예제.

Dify 의 워크플로(Start → LLM/Code/... → End)는 `graphon` 패키지가 실행한다.
여기서는 LLM 대신 직접 만든 커스텀 노드(UppercaseNode)를 끼워
  Start(query) → Uppercase → End(result)
그래프를 구성하고 GraphEngine 이 내보내는 이벤트를 출력한다.

Dify 실제 코드:
  - api/core/workflow/node_factory.py  (DifyNodeFactory: 노드 type → Node 클래스)
  - api/core/workflow/workflow_entry.py (GraphEngine 생성/실행)
"""

import time
from typing import override

from graphon.entities.base_node_data import BaseNodeData
from graphon.entities.graph_config import NodeConfigDict
from graphon.entities.graph_init_params import GraphInitParams
from graphon.enums import BuiltinNodeTypes, NodeType, WorkflowNodeExecutionStatus
from graphon.graph import Graph
from graphon.graph_engine import GraphEngine, GraphEngineConfig
from graphon.graph_engine.command_channels import InMemoryChannel
from graphon.graph_events import GraphRunSucceededEvent, NodeRunStartedEvent, NodeRunSucceededEvent
from graphon.node_events import NodeRunResult
from graphon.nodes.base.node import Node
from graphon.nodes.end.end_node import EndNode
from graphon.nodes.end.entities import EndNodeData
from graphon.nodes.start.entities import StartNodeData
from graphon.nodes.start.start_node import StartNode
from graphon.runtime import GraphRuntimeState, VariablePool


# ---------------------------------------------------------------------------
# 1) 커스텀 노드: 이전 노드 출력(selector)을 대문자로 바꿔 출력한다.
# ---------------------------------------------------------------------------
class UppercaseNodeData(BaseNodeData):
    type: NodeType = "uppercase"
    source: list[str]  # 예: ["start", "query"] → start 노드의 query 출력


class UppercaseNode(Node[UppercaseNodeData]):
    node_type = "uppercase"

    @classmethod
    @override
    def version(cls) -> str:
        return "1"

    @override
    def _run(self) -> NodeRunResult:
        segment = self.graph_runtime_state.variable_pool.get(self.node_data.source)
        text = segment.text if segment else ""
        return NodeRunResult(
            status=WorkflowNodeExecutionStatus.SUCCEEDED,
            inputs={"text": text},
            outputs={"text": text.upper()},
        )


# ---------------------------------------------------------------------------
# 2) NodeFactory: 그래프 JSON 의 node.data.type 을 보고 Node 인스턴스를 만든다.
# ---------------------------------------------------------------------------
class SimpleNodeFactory:
    registry: dict[str, tuple[type[Node], type[BaseNodeData]]] = {
        BuiltinNodeTypes.START: (StartNode, StartNodeData),
        BuiltinNodeTypes.END: (EndNode, EndNodeData),
        "uppercase": (UppercaseNode, UppercaseNodeData),
    }

    def __init__(self, init_params: GraphInitParams, runtime_state: GraphRuntimeState):
        self.init_params = init_params
        self.runtime_state = runtime_state

    def create_node(self, node_config: NodeConfigDict) -> Node:
        raw = node_config["data"]
        raw_dict = raw if isinstance(raw, dict) else raw.model_dump()
        node_cls, data_cls = self.registry[raw_dict["type"]]
        return node_cls(
            node_config["id"],
            data_cls.model_validate(raw_dict),
            graph_init_params=self.init_params,
            graph_runtime_state=self.runtime_state,
        )


# ---------------------------------------------------------------------------
# 3) 그래프 정의 — Dify 가 DB(workflows.graph)에 저장하는 JSON 과 같은 모양
# ---------------------------------------------------------------------------
GRAPH = {
    "nodes": [
        {"id": "start", "data": {"type": "start", "title": "Start", "variables": []}},
        {"id": "upper", "data": {"type": "uppercase", "title": "Upper", "source": ["start", "query"]}},
        {
            "id": "end",
            "data": {
                "type": "end",
                "title": "End",
                "outputs": [{"variable": "result", "value_selector": ["upper", "text"]}],
            },
        },
    ],
    "edges": [
        {"id": "e1", "source": "start", "target": "upper"},
        {"id": "e2", "source": "upper", "target": "end"},
    ],
}


def main() -> None:
    init_params = GraphInitParams(workflow_id="demo", graph_config=GRAPH, run_context={}, call_depth=0)

    # VariablePool: 노드 간 데이터가 오가는 공용 저장소. (node_id, var_name) 으로 접근
    pool = VariablePool()
    pool.add(["start", "query"], "hello dify workflow")
    runtime_state = GraphRuntimeState(variable_pool=pool, start_at=time.perf_counter())

    graph = Graph.init(
        graph_config=GRAPH,
        node_factory=SimpleNodeFactory(init_params, runtime_state),
        root_node_id="start",
    )
    engine = GraphEngine(
        workflow_id="demo",
        graph=graph,
        graph_runtime_state=runtime_state,
        command_channel=InMemoryChannel(),  # 외부에서 abort/pause 명령을 보내는 채널
        config=GraphEngineConfig(),
    )

    for event in engine.run():  # 이벤트 스트림 → Dify 는 이것을 SSE 로 프론트에 전달
        match event:
            case NodeRunStartedEvent():
                print(f"[node start]   {event.node_id}")
            case NodeRunSucceededEvent():
                print(f"[node success] {event.node_id} outputs={dict(event.node_run_result.outputs)}")
            case GraphRunSucceededEvent():
                print(f"[graph done]   outputs={event.outputs}")
            case _:
                print(f"[event]        {type(event).__name__}")


if __name__ == "__main__":
    main()
