import spacy
import sentence_extractor as sente
from rdflib import Graph, Namespace
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt

PREFIX = Namespace("prefix://")


def normalize_triplet(triplet):
    return [term.replace(" ", "_") for term in triplet]


def print_graph(graph):
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


def build_graph(triplets):
    g = Graph()

    for triplet in triplets:
        triplet = normalize_triplet(triplet)
        subject, relation, _object = triplet
        g.add((PREFIX[subject], PREFIX[relation], PREFIX[_object]))

    return g


def main():
    nlp = spacy.load("en_core_web_sm")  # English tokenizer

    with open("./input.txt") as file:
        text = file.read()

    doc = nlp(text)

    triplets = sente.findSVOs(doc)
    agroGraph = build_graph(triplets)
    agroGraph.serialize("output.ttl", format="turtle", encoding="utf-8")
    print_graph(agroGraph)


if __name__ == "__main__":
    main()
