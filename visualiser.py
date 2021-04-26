import re
import time
import yaml
import argparse
import graphviz
import pandas as pd

from utils import Node, Edge
from benchmarks import *

parser = argparse.ArgumentParser(description="Fast cell visualisation")
parser.add_argument("--arch", default=1, type=int)
parser.add_argument("--save", action="store_true")
parser.add_argument(
    "--df_loc", default="minibench/mini-bench-arch-cell-accs.pd", type=str
)
parser.add_argument(
    "--stylesheet",
    default="stylesheets/default.yaml",
    type=str,
    help="Path to a yaml file containing the style preferences for your graph.",
)
args: argparse.Namespace = parser.parse_args()

if __name__ == "__main__":

    df: pd.DataFrame = pd.read_pickle("minibench/mini-bench-arch-cell-accs.pd")

    with open(args.stylesheet, "r") as file:
        stylesheet: object = yaml.safe_load(file)

    graph: NASBenchDigraph = NASBench201Digraph(df, stylesheet)

    node_str: str = graph.get_cell_description(args.arch)
    nodes, edges = graph.parse_cell(node_str)

    for node in nodes:
        graph.add_node(node)

    for edge in edges:
        graph.add_edge(edge)

    dot: graphviz.Digraph = graph.dot_graph

    dot.render(view=True)

    if args.save:
        dot.render(f"render/{args.arch}.gv")
