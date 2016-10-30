"""Conversion between rdflib and PyLD data formats for compatibility.

Unfortunately these two libraries use different in-memory data structures
so it is not trivial to use the power RDF support of rdflib in conjuction
with the JSON-LD processor implementation of PyLD. This code is designed
to provide a bridge from rdflib->PyLD formats without the need to
serialize and then re-parse the data.

rdflib: see <http://rdflib.readthedocs.io/en/stable/apidocs/>

PyLD: see <https://github.com/digitalbazaar/pyld>
"""

from rdflib import Graph, URIRef, Literal, BNode
from pyld import jsonld


def rdflib_term_to_pyld_term(term):
    """Convert rdflib term to a PyLD term.

    See:
    <http://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#module-rdflib.term>
    and
    <https://github.com/digitalbazaar/pyld/blob/master/lib/pyld/jsonld.py#L1645>a

    Return value is a PyLD term which is represented as a hash where:
      `type` in {'IRI', 'blank node', 'literal'}
      `value` is string of IRI, BNoode or literal
      `language` optional language code for literal, else None
      `datatype` optional data type URI for literal, else None
    """
    t = {'type': 'IRI',
         'value': str(term)}
    if (isinstance(term, BNode)):
        t['type'] = 'blank node'
    elif (isinstance(term, Literal)):
        t['type'] = 'literal'
        t['datatype'] = str(term.datatype) if (term.datatype) else None
        t['language'] = str(term.language) if (term.language) else None
    return(t)


def pyld_graph_from_rdflib_graph(graph):
    """Get a PyLD dataset from an rdflib graph.

    Returns the contents of the input graph in the @default graph of
    the output dataset.
    """
    g = []
    for s, p, o in graph:
        triple = {}
        triple['subject'] = rdflib_term_to_pyld_term(s)
        triple['predicate'] = rdflib_term_to_pyld_term(p)
        triple['object'] = rdflib_term_to_pyld_term(o)
        g.append(triple)
    return g


def pyld_json_from_rdflib_graph(graph):
    """Get PyLD JSON object from and rdflib input graph."""
    return jsonld.from_rdf({'@default': pyld_graph_from_rdflib_graph(graph)})
