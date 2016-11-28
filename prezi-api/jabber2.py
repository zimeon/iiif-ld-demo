"""Step 1 preparing Jabberwocky manifest."""
from rdflib import Graph, BNode, Literal
from rdflib.namespace import Namespace, RDF, RDFS, DC, XSD
from rdflib_pyld_compat import pyld_json_from_rdflib_graph
from pyld import jsonld
import context_cache.for_pyld
import json
import sys

sc = Namespace("http://iiif.io/api/presentation/2#")
oa = Namespace("http://www.w3.org/ns/oa#")
jw = Namespace("http://localhost:8000/jabberwocky/")


def StrLiteral(s):
    """String literal convenience method."""
    return Literal(s, datatype=XSD.string)

# Build RDF
g = Graph()
g.add((jw.manifest, RDF.type, sc.Manifest))
# Simple descriptive information
g.add((jw.manifest, RDFS.label, StrLiteral("Jabberwocky")))
g.add((jw.manifest, DC.description,
       StrLiteral("A bad edition of wonderful nonsense.")))
# Label/value pairs
author = BNode()
g.add((jw.manifest, sc.metadataLabels, author))
g.add((author, RDFS.label, StrLiteral("Author")))
g.add((author, RDF.value, StrLiteral("Lewis Carroll")))

# Get JSON-LD object in PyLD form
jld = pyld_json_from_rdflib_graph(g)

# Frame and compact...
framed = jsonld.compact(
    jsonld.frame(jld, "http://iiif.io/api/presentation/2/manifest_frame.json"),
    "http://iiif.io/api/presentation/2/context.json")
print(json.dumps(framed, indent=2, sort_keys=True))
