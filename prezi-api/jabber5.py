"""Step 5 preparing Jabberwocky manifest."""
from rdflib import Graph, BNode, Literal
from rdflib.namespace import Namespace, RDF, RDFS, DC, XSD
from rdflib_pyld_compat import pyld_jsonld_from_rdflib_graph
from pyld import jsonld
import context_cache.for_pyld
import json
import sys

sc = Namespace("http://iiif.io/api/presentation/2#")
oa = Namespace("http://www.w3.org/ns/oa#")
exif = Namespace("http://www.w3.org/2003/12/exif/ns#")
dctypes = Namespace("http://purl.org/dc/dcmitype/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
jw = Namespace("http://localhost:8000/jabberwocky/")


def StrLiteral(s):
    """String literal convenience method."""
    return Literal(s, datatype=XSD.string)


def ListStart(g, s, p, f=None):
    """Add first element of RDF:List, return list and first."""
    l = BNode()
    if (f is None):
        f = BNode()
    g.add((s, p, l))
    g.add((l, RDF.type, RDF.List))
    g.add((l, RDF.first, f))
    g.add((l, RDF.rest, RDF.nil))
    return(l, f)


def ListAdd(g, prev, f=None):
    """Add another element to RDF:List prev, return new list and first."""
    l = BNode()
    if (f is None):
        f = BNode()
    g.remove((prev, RDF.rest, RDF.nil))
    g.add((prev, RDF.rest, l))
    g.add((l, RDF.type, RDF.List))
    g.add((l, RDF.first, f))
    g.add((l, RDF.rest, RDF.nil))
    return(l, f)

# Build RDF
g = Graph()
manifest = jw['manifest.json']
g.add((manifest, RDF.type, sc.Manifest))
# Simple descriptive information
g.add((manifest, RDFS.label, StrLiteral("Jabberwocky")))
g.add((manifest, DC.description,
       StrLiteral("A bad edition of wonderful nonsense.")))
# List of label/value pairs
(ml1, author) = ListStart(g, manifest, sc.metadataLabels)
g.add((author, RDFS.label, StrLiteral("Author")))
g.add((author, RDF.value, StrLiteral("Lewis Carroll")))
(ml2, pub_year) = ListAdd(g, ml1)
g.add((pub_year, RDFS.label, StrLiteral("Published")))
g.add((pub_year, RDF.value, StrLiteral("1871")))

# Sequence of canvases
(sequences, seq) = ListStart(g, manifest, sc.hasSequences)
g.add((seq, RDF.type, sc.Sequence))
g.add((seq, RDFS.label, StrLiteral("Normal Page Order")))
(cl1, c1) = ListStart(g, seq, sc.hasCanvases, jw['canvas/1'])
g.add((c1, RDF.type, sc.Canvas))
(cl2, c2) = ListAdd(g, cl1, jw['canvas/2'])
g.add((c2, RDF.type, sc.Canvas))

# Add images on the canvases
g.add((c1, RDFS.label, StrLiteral('c1')))
g.add((c1, exif.height, Literal(4000, datatype=XSD.integer)))
g.add((c1, exif.width, Literal(3000, datatype=XSD.integer)))
g.add((c1, foaf.thumbnail, jw['image/fcr_thumb.jpg']))
(c1imgs, c1img1) = ListStart(g, c1, sc.hasImageAnnotations)
g.add((c1img1, RDF.type, oa.Annotation))
g.add((c1img1, oa.motivatedBy, sc.painting))
img1 = jw['image/fcr.jpg']
g.add((c1img1, oa.hasBody, img1))
g.add((img1, RDF.type, dctypes.Image))
g.add((c1img1, oa.hasTarget, c1))

g.add((c2, RDFS.label, StrLiteral('c2')))
g.add((c2, exif.height, Literal(4000, datatype=XSD.integer)))
g.add((c2, exif.width, Literal(3000, datatype=XSD.integer)))
g.add((c2, foaf.thumbnail, jw['image/fcv_thumb.jpg']))
(c2imgs, c2img2) = ListStart(g, c2, sc.hasImageAnnotations)
g.add((c2img2, RDF.type, oa.Annotation))
# g.add((c2img2, oa.motivatedBy, sc.painting))
img2 = jw['image/fcv.jpg']
g.add((c2img2, oa.hasBody, img2))
g.add((img2, RDF.type, dctypes.Image))
g.add((c2img2, oa.hasTarget, c2))

# Get JSON-LD object in PyLD form
jld = pyld_jsonld_from_rdflib_graph(g)

# Frame and compact...
framed = jsonld.compact(
    jsonld.frame(jld, "http://iiif.io/api/presentation/2/manifest_frame.json"),
    "http://iiif.io/api/presentation/2/context.json")
with open('jabberwocky/manifest.json', 'w') as fh:
    json.dump(framed, fh, indent=2, sort_keys=True)
