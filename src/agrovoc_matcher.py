# import spacy
from spikex.wikigraph import load as wg_load
from spikex.pipes import WikiPageX
from consts import (
    # WIKIPEDIA_URL,
    BASE_AGROVOC_URL,
    SKOS_PREFIX,
    AGROVOC_PREFIX,
    LOCAL_GRAPH_PREFIX as PREFIX,
)
import requests as rq
from bs4 import BeautifulSoup
from rdflib import Graph
from utils import normalize_resource


def find_wikipedia_articles(tokens):
    wg = wg_load("simplewiki_core")
    wpx = WikiPageX(wg)

    doc = wpx(tokens)
    return doc._.wiki_spans


def get_agrovoc_triplets(concept):
    """
    Recives a concept/word and if found returns agrovoc's broader and narrower concepts
    """
    if concept_URI := search_agrovoc_concept(concept):
        graph = create_remote_graph(concept_URI)
        # Remove the URL prefix from the ID, wich has a length of 47 chars
        # https://agrovoc.fao.org/browse/agrovoc/en/page/<ID>
        concept_ID = concept_URI[47:]
        agrovoc_data = get_related_triplets(graph, concept_ID)
        agrovoc_data.append(
            (
                PREFIX[normalize_resource(concept)],
                PREFIX["is_agrovoc"],
                AGROVOC_PREFIX[concept_ID],
            )
        )
        return agrovoc_data
    else:
        return []


def search_agrovoc_concept(concept):
    response = rq.get(f"{BASE_AGROVOC_URL}agrovoc/en/search?clang=en&q={concept}")
    if not response.ok:
        return None

    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.findAll("a", class_="conceptlabel")
    if anchors:
        URI = BASE_AGROVOC_URL + anchors[0].attrs["href"]
        return URI
    else:
        return None


def create_remote_graph(URI):
    html = rq.get(URI).text
    soup = BeautifulSoup(html, "html.parser")
    turtle_anchors = soup.select("span.versal.concept-download-links > a:nth-child(1)")
    link = turtle_anchors[0].attrs["href"]
    g = Graph()
    g.parse(BASE_AGROVOC_URL + link)

    return g


def get_related_triplets(g, subject_id):
    broader_concepts = g.triples(
        (AGROVOC_PREFIX[subject_id], SKOS_PREFIX["broader"], None)
    )
    narrower_concepts = g.triples(
        (None, SKOS_PREFIX["broader"], AGROVOC_PREFIX[subject_id])
    )
    return list(broader_concepts) + list(narrower_concepts)


# def main():
#     nlp = spacy.load("en_core_web_sm")  # English tokenizer

#     with open("../data/input.txt") as file:
#         text = file.read()

#     doc = nlp(text)
#     wiki_words = find_wikipedia_articles(doc)
#     for word in wiki_words:
#         print(word, "---> ", word._.wiki_pages)


# if __name__ == "__main__":
#     main()
