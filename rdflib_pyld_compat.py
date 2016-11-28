"""Conversion between rdflib and PyLD data formats for compatibility.

Unfortunately these two libraries use different in-memory data structures
so it is not trivial to use the power RDF support of rdflib in conjuction
with the JSON-LD processor implementation of PyLD. This code is designed
to provide a bridge from rdflib->PyLD formats without the need to
serialize and then re-parse the data.

rdflib: see <http://rdflib.readthedocs.io/en/stable/apidocs/>

PyLD: see <https://github.com/digitalbazaar/pyld>

FIXME - this is limited in that it assumes the URIRefs in the rdflib graph
do not need expansion with a namespaceManager.
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
      `language` optional language code for literal (if present `datatype` will
          default to RDF.langString)
      `datatype` optional data type URI for literal, else None
    """
    t = {'type': 'IRI',
         'value': str(term)}
    if (isinstance(term, BNode)):
        t['type'] = 'blank node'
        t['value'] = '_:' + t['value']
    elif (isinstance(term, Literal)):
        t['type'] = 'literal'
        if (term.language):
            t['datatype'] = str(term.datatype) if (term.datatype) else \
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#langString'
            t['language'] = str(term.language)
        else:
            t['datatype'] = str(term.datatype) if (term.datatype) else None
    return(t)


def pyld_graph_from_rdflib_graph(graph):
    """Get a PyLD dataset from an rdflib graph.

    Returns the contents of the input graph as a list if triples where
    each triple is represented as a dict with term entries for 'subject',
    'predicate', and 'object'.
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
    default_graph = pyld_graph_from_rdflib_graph(graph)
    return jsonld.from_rdf({'@default': default_graph})
