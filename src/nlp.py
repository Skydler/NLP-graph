from rdflib import Graph
from consts import PREFIX
from utils import normalize_triplet, print_rdflib_graph
import spacy

import sentence_extractor as sente


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
    print_rdflib_graph(agroGraph)


if __name__ == "__main__":
    main()
