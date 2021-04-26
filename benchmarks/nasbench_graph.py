import graphviz
from utils import Node, Edge
from abc import abstractmethod
from typing import Optional, Tuple, List

__all__ = ["NASBenchDigraph"]


class NASBenchDigraph:
    def __init__(self) -> None:
        self.OPS: Optional[List[str]] = None
        self.dot_graph: graphviz.Digraph = None

    def add_node(self, node: Node) -> None:
        self.dot_graph.node(node.id, node.label)

    def add_edge(self, edge: Edge) -> None:
        self.dot_graph.edge(edge.from_node_id, edge.to_node_id, edge.label)

    @abstractmethod
    def get_cell_description(self, arch: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_cell(self, cell_str: str) -> Tuple[List[Node], List[Edge]]:
        raise NotImplementedError
