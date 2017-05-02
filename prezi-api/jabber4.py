"""Step 4 preparing Jabberwocky manifest."""
from rdflib import Graph, BNode, Literal
from rdflib.namespace import Namespace, RDF, RDFS, DC, XSD
from rdflib_pyld_compat import pyld_jsonld_from_rdflib_graph
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


def ListStart(g, s, p):
    """Add first element of RDF:List, return list and first."""
    l = BNode()
    f = BNode()
    g.add((s, p, l))
    g.add((l, RDF.type, RDF.List))
    g.add((l, RDF.first, f))
    g.add((l, RDF.rest, RDF.nil))
    return(l, f)


def ListAdd(g, l):
    """Add another element to RDF:List l, return new list and first."""
    l2 = BNode()
    f = BNode()
    g.remove((l, RDF.rest, RDF.nil))
    g.add((l, RDF.rest, l2))
    g.add((l2, RDF.type, RDF.List))
    g.add((l2, RDF.first, f))
    g.add((l2, RDF.rest, RDF.nil))
    return(l2, f)

# Build RDF
g = Graph()
g.add((jw.manifest, RDF.type, sc.Manifest))
# Simple descriptive information
g.add((jw.manifest, RDFS.label, StrLiteral("Jabberwocky")))
g.add((jw.manifest, DC.description,
       StrLiteral("A bad edition of wonderful nonsense.")))
# List of label/value pairs
(ml1, author) = ListStart(g, jw.manifest, sc.metadataLabels)
g.add((author, RDFS.label, StrLiteral("Author")))
g.add((author, RDF.value, StrLiteral("Lewis Carroll")))
(ml2, pub_year) = ListAdd(g, ml1)
g.add((pub_year, RDFS.label, StrLiteral("Published")))
g.add((pub_year, RDF.value, StrLiteral("1871")))

# Sequence of canvases
(sequences, seq) = ListStart(g, jw.manifest, sc.hasSequences)
g.add((seq, RDF.type, sc.Sequence))
g.add((seq, RDFS.label, StrLiteral("Normal Page Order")))
(cl1, c1) = ListStart(g, seq, sc.hasCanvases)
g.add((c1, RDF.type, sc.Canvas))
(cl2, c2) = ListAdd(g, cl1)
g.add((c2, RDF.type, sc.Canvas))

# Get JSON-LD object in PyLD form
jld = pyld_jsonld_from_rdflib_graph(g)

# Frame and compact...
framed = jsonld.compact(
    jsonld.frame(jld, "http://iiif.io/api/presentation/2/manifest_frame.json"),
    "http://iiif.io/api/presentation/2/context.json")
print(json.dumps(framed, indent=2, sort_keys=True))
