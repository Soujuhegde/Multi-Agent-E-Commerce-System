from src.graph.graph_builder import (
    build_graph
)

graph = build_graph()


class WorkflowExecutor:

    @staticmethod
    def execute(
        query: str
    ):

        state = {
            "user_query": query
        }

        result = graph.invoke(
            state
        )

        return result