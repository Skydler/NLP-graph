import matplotlib.pyplot as plt
import networkx as nx
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
from consts import PREFIX


def normalize_triplet(triplet):
    return [term.replace(" ", "_") for term in triplet]


def print_rdflib_graph(graph):
    nxGraph = rdflib_to_networkx_multidigraph(
        graph, edge_attrs=lambda s, p, o: {"label": p.removeprefix(PREFIX)}
    )

    pos = nx.spring_layout(nxGraph, k=1, scale=2)
    nx.draw_networkx(nxGraph, pos=pos, with_labels=True)
    nx.draw_networkx_edge_labels(
        nxGraph,
        pos=pos,
        edge_labels={(u, v): d["label"] for u, v, d in nxGraph.edges(data=True)},
    )

    plt.show()
