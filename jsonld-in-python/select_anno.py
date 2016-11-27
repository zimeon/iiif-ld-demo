"""Example of preparation with rdflib, JSON-LD manip with PyLD."""
from rdflib import Graph, URIRef
from rdflib.namespace import Namespace, RDF
from rdflib_pyld_compat import pyld_json_from_rdflib_graph
from pyld import jsonld
import json
import sys

# Build test graph in rdflib
# -- no easy way to do this is PyLD
g1 = Graph()
sc = Namespace("http://iiif.io/api/presentation/2#")
oa = Namespace("http://www.w3.org/ns/oa#")
ex = Namespace("http://example.org/")

g1.add((ex.anno1, RDF.type, oa.Annotation))
g1.add((ex.anno1, oa.motivatedBy, ex.Drawing))
g1.add((ex.anno1, oa.hasBody, ex.hand1))
g1.add((ex.anno1, oa.hasTarget, ex.hand2))

g1.add((ex.anno2, RDF.type, oa.Annotation))
g1.add((ex.anno2, oa.motivatedBy, ex.Drawing))
g1.add((ex.anno2, oa.hasBody, ex.hand2))
g1.add((ex.anno2, oa.hasTarget, ex.hand1))

# Manipulate the graph using rdflib. Select all annotiations
# with targets given on the command line
# -- no easy way to do this in PyLD
g2 = Graph()
for target in sys.argv[1:]:
    for anno in g1[:oa.hasTarget:URIRef(target)]:
        g2 += g1.triples((anno, None, None))

# Get JSON-LD object in PyLD form
jld = pyld_json_from_rdflib_graph(g2)

# Apply context in PyLD
context = {"@context": [{
  "id": "@id",
  "type": "@type",
  "oa": "http://www.w3.org/ns/oa#",
  "motivation": {"@type": "@id", "@id": "oa:motivatedBy"},
  "resource": {"@type": "@id", "@id": "oa:hasBody"},
  "on": {"@type": "@id", "@id": "oa:hasTarget"}
  }]
}

# Manipulate the JSON in some way (say switch @context
# to a reference) and output
# -- no easy way to do this is rdflib
comp = jsonld.compact(jld, context)
comp['@context'] = str(ex.context)
print(json.dumps(comp, indent=2, sort_keys=True))
