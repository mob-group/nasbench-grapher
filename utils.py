from dataclasses import dataclass
from typing import Optional

__all__ = ["Node", "Edge"]


@dataclass(unsafe_hash=True)
class Node:
    id: str
    label: Optional[str] = None


@dataclass(unsafe_hash=True)
class Edge:
    from_node_id: str
    to_node_id: str
    label: Optional[str] = None
