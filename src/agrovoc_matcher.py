import logging

from SPARQLWrapper import SPARQLWrapper
from rdflib import OWL, SKOS

from consts import LOCAL_GRAPH_PREFIX as PREFIX, RELATED_CONCEPTS_QUERY
from utils import normalize_resource


def extend_with_agrovoc(g, concept):
    """
    Recives a concept/word and if found returns agrovoc's broader and narrower concepts
    """

    normalized_concept = normalize_resource(concept)

    # Prevent further requests if it's already processed
    if (PREFIX[normalized_concept], OWL.sameAs, None) in g:
        return

    new_graph = query_agrovoc(concept)
    if new_graph:
        logging.info(f'Concept "{concept}" found in agrovoc, extracting data...')
        concept_URI = get_concept_URI(new_graph)

        # Add local connection to the graph created
        g.add((PREFIX[normalized_concept], OWL.sameAs, concept_URI))
        g += new_graph


def query_agrovoc(concept):
    sparql = SPARQLWrapper("https://agrovoc.fao.org/sparql")
    query = RELATED_CONCEPTS_QUERY.format(concept=concept)
    sparql.setQuery(query)
    results = sparql.queryAndConvert()
    return results


def get_concept_URI(g):
    subject, _, _ = next(g.triples((None, SKOS.narrower, None)))
    return subject
