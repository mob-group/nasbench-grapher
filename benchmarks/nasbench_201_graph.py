import re
import graphviz
import numpy as np
import pandas as pd

from utils import Node, Edge
from typing import List, Optional, Tuple, Set

from .nasbench_graph import NASBenchDigraph

__all__ = ["NASBench201Digraph"]


class NASBench201Digraph(NASBenchDigraph):
    OPS: List[str] = ["conv_3x3", "conv_1x1", "avg_pool_3x3", "skip_connect", "none"]
    PRETTY_OPS: List[str] = ["Conv(3,3)", "Conv(1,1)", "AvgPool2d(3,3)", "Skip", "None"]

    pretty_names: dict = {
        "conv_3x3": "Conv(3,3)",
        "conv_1x1": "Conv(1,1)",
        "avg_pool_3x3": "AvgPool2d(3,3)",
        "skip_connect": "Skip",
        "none": "None",
    }

    def __init__(self, df: pd.DataFrame, stylesheet: Optional[dict] = None) -> None:

        self.dot_graph: graphviz.Digraph = graphviz.Digraph(
            format="pdf",
            edge_attr=stylesheet["edge_attr"] if stylesheet is not None else {},
            node_attr=stylesheet["node_attr"] if stylesheet is not None else {},
            engine="dot",
        )

        # left to right
        self.dot_graph.body.extend(["rankdir=LR"])

        # get bench api
        self.df = df

        # add input node
        self.add_node(Node("0", "in"))

    def add_node(self, node: Node) -> None:
        if node.id == "3":
            self.dot_graph.node(node.id, label="out")
        else:
            self.dot_graph.node(node.id, node.label)

    def get_cell_description(self, arch_num: int = 1) -> str:
        nodestr: str = self.df.iloc[arch_num]["cellstr"]
        nodestr = nodestr[1:-1]  # remove leading and trailing bars |
        nodestr = self.remove_pointless_ops(nodestr)

        return nodestr

    def parse_cell(self, cell_str: str) -> Tuple[List[Node], List[Edge]]:
        # remove leading and trailing bars |

        if cell_str[0] == "|":
            cell_str: str = cell_str[1:]

        if cell_str[-1] == "|":
            cell_str = cell_str[:-1]

        nodes: Set[Node] = set()
        edges: Set[Edge] = set()

        # e.g.
        # |nor_conv_3x3~0|+|nor_conv_3x3~0|avg_pool_3x3~1|+|skip_connect~0|nor_conv_3x3~1|skip_connect~2|
        for i, node in enumerate(cell_str.split("|+|")):
            node_id: int = i + 1
            #  e.g.
            # skip_connect~0|nor_conv_3x3~1|skip_connect~2|
            for op_str in node.split("|"):

                #  e.g.
                #  skip_connect~0
                nodes.add(Node(f"{node_id}"))
                op_name: str = [self.pretty_names[o] for o in self.OPS if o in op_str][
                    0
                ]

                connected_from: list = re.findall("~[0-9]", op_str)

                if len(connected_from) > 0:
                    connected_from = connected_from[0][1:]
                    edges.add(Edge(f"{connected_from}", f"{node_id}", op_name))

        return list(nodes), list(edges)

    def set_none(self, bit: str) -> str:
        tmp = bit.split("~")
        tmp[0] = "none"
        return "~".join(tmp)

    def remove_pointless_ops(self, archstr: str) -> str:
        old = None
        new = archstr
        while old != new:
            old = new
            bits = old.strip("|").split("|")
            if "none~" in bits[0]:  # node 1 has no connections to it
                bits[3] = self.set_none(bits[3])  # node 1 -> 2 now none
                bits[6] = self.set_none(bits[6])  # node 1 -> 3 now none
            if (
                "none~" in bits[2] and "none~" in bits[3]
            ):  # node 2 has no connections to it
                bits[7] = self.set_none(bits[7])  # node 2 -> 3 now none
            if "none~" in bits[7]:  # doesn't matter what comes through node 2
                bits[2] = self.set_none(bits[2])  # node 0 -> 2 now none
                bits[3] = self.set_none(bits[3])  # node 1 -> 2 now none
            if (
                "none~" in bits[6] and "none~" in bits[7]
            ):  # doesn't matter what comes through node 1
                bits[0] = self.set_none(bits[0])  # node 0 -> 1 now none
            new = "|".join(bits)
        return new

    def compile_graph_to_matrix(self, nodes: List[Node], edges: List[Edge]):
        # nodes = [0,1,2,3]
        # edges = [Edge(0,1,'conv1x1'), Edge(1,2,'conv3x3')]

        matrix = np.zeros((len(nodes), len(self.OPS)))

        for edge in edges:
            matrix[
                int(edge.from_node_id), int(edge.to_node_id)
            ] = self.PRETTY_OPS.index(edge.label)

        return matrix
