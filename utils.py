import graphviz
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Optional

__all__ = ["Node", "Edge", "NASBenchDigraph"]


@dataclass(unsafe_hash=True)
class Node:
    id: str
    label: Optional[str] = None


@dataclass(unsafe_hash=True)
class Edge:
    from_node_id: str
    to_node_id: str
    label: Optional[str] = None


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
