import logging

from rdflib import Graph, SKOS
import requests as rq

from consts import AGROVOC_PREFIX, BASE_AGROVOC_URL, LOCAL_GRAPH_PREFIX as PREFIX
from utils import normalize_resource


def extend_with_agrovoc(g, concept):
    """
    Recives a concept/word and if found returns agrovoc's broader and narrower concepts
    """

    normalized_concept = normalize_resource(concept)

    # Prevent further requests if it's already processed
    if (PREFIX[normalized_concept], PREFIX["is_agrovoc"], None) in g:
        return

    concept_URI = search_agrovoc_concept(concept)
    if not concept_URI:
        return

    logging.info(f'Concept "{concept}" found in agrovoc, extracting data...')
    graph = create_remote_graph(concept_URI)

    concept_ID = concept_URI.removeprefix("http://aims.fao.org/aos/agrovoc/")
    g.add(
        (
            PREFIX[normalized_concept],
            PREFIX["is_agrovoc"],
            AGROVOC_PREFIX[concept_ID],
        )
    )

    agrovoc_data = get_related_triplets(graph, concept_ID)
    for triplet in agrovoc_data:
        g.add(triplet)


def search_agrovoc_concept(concept):
    response = rq.get(f"{BASE_AGROVOC_URL}rest/v1/search?query={concept}*&lang=en")
    response.raise_for_status()

    data = response.json()

    if URIS := data.get("results"):
        return URIS[0].get("uri")  # Return the first match
    return None


def create_remote_graph(URI):
    g = Graph().parse(URI)
    return g


def get_related_triplets(g, subject_id):
    broader_concepts = g.triples((AGROVOC_PREFIX[subject_id], SKOS.narrower, None))
    narrower_concepts = g.triples((None, SKOS.broader, AGROVOC_PREFIX[subject_id]))
    return list(broader_concepts) + list(narrower_concepts)
