from rdflib import Graph
import spacy
from consts import LOCAL_GRAPH_PREFIX as PREFIX
import sentence_extractor as sente
from utils import normalize_triplet, print_rdflib_graph
from agrovoc_matcher import get_agrovoc_triplets


def build_graph(triplets):
    g = Graph()

    for triplet in triplets:
        subject, relation, _object = normalize_triplet(triplet)
        g.add((PREFIX[subject], PREFIX[relation], PREFIX[_object]))

        raw_s, _, raw_o = triplet
        extra_triplets = get_agrovoc_triplets(raw_s) + get_agrovoc_triplets(raw_o)
        for triplet in extra_triplets:
            g.add(triplet)

    return g


def main():
    nlp = spacy.load("en_core_web_sm")  # English tokenizer

    with open("../data/input.txt") as file:
        text = file.read()

    doc = nlp(text)

    triplets = sente.findSVOs(doc)
    agroGraph = build_graph(triplets)

    agroGraph.serialize("../data/output.ttl", format="turtle", encoding="utf-8")
    print_rdflib_graph(agroGraph)


if __name__ == "__main__":
    main()
