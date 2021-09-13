from rdflib import Namespace

LOCAL_GRAPH_PREFIX = Namespace("prefix://")
AGROVOC_PREFIX = Namespace("http://aims.fao.org/aos/agrovoc/")
BASE_AGROVOC_URL = "https://agrovoc.fao.org/browse/"

RELATED_CONCEPTS_QUERY = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
CONSTRUCT {{
  ?subject skos:narrower ?narrower.
  ?subject skos:broader ?broader
}}
WHERE {{
  ?subject skos:prefLabel "{concept}"@en.
  ?subject skos:narrower ?narrower.
  ?subject skos:broader ?broader
}}
"""
