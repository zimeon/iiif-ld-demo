"""Step 1 preparing Jabberwocky manifest."""
from rdflib import Graph
from rdflib.namespace import Namespace, RDF
from rdflib_pyld_compat import pyld_json_from_rdflib_graph
from pyld import jsonld
import context_cache.for_pyld
import json
import sys

sc = Namespace("http://iiif.io/api/presentation/2#")
oa = Namespace("http://www.w3.org/ns/oa#")
jw = Namespace("http://localhost:8000/jabberwocky/")

# Build RDF
g = Graph()
g.add((jw.manifest, RDF.type, sc.Manifest))

# Get JSON-LD object in PyLD form
jld = pyld_json_from_rdflib_graph(g)

# Frame and compact...
framed = jsonld.compact(
    jsonld.frame(jld, "http://iiif.io/api/presentation/2/manifest_frame.json"),
    "http://iiif.io/api/presentation/2/context.json")
print(json.dumps(framed, indent=2, sort_keys=True))
