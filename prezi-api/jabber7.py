"""Step 6 preparing Jabberwocky manifest."""
from rdflib import Graph, BNode, Literal, URIRef
from rdflib.namespace import Namespace, RDF, RDFS, DC, XSD
from rdflib_pyld_compat import pyld_json_from_rdflib_graph
from pyld import jsonld
import context_cache.for_pyld
import json
import sys

sc = Namespace("http://iiif.io/api/presentation/2#")
oa = Namespace("http://www.w3.org/ns/oa#")
exif = Namespace("http://www.w3.org/2003/12/exif/ns#")
dctypes = Namespace("http://purl.org/dc/dcmitype/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
svcs = Namespace("http://rdfs.org/sioc/services#")
doap = Namespace("http://usefulinc.com/ns/doap#")
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
(cl3, c3) = ListAdd(g, cl2, jw['canvas/3'])
g.add((c3, RDF.type, sc.Canvas))
(cl4, c4) = ListAdd(g, cl3, jw['canvas/4'])
g.add((c4, RDF.type, sc.Canvas))
(cl5, c5) = ListAdd(g, cl4, jw['canvas/5'])
g.add((c5, RDF.type, sc.Canvas))
(cl6, c6) = ListAdd(g, cl5, jw['canvas/6'])
g.add((c6, RDF.type, sc.Canvas))
(cl7, c7) = ListAdd(g, cl6, jw['canvas/7'])
g.add((c7, RDF.type, sc.Canvas))
(cl8, c8) = ListAdd(g, cl7, jw['canvas/8'])
g.add((c8, RDF.type, sc.Canvas))
(cl9, c9) = ListAdd(g, cl8, jw['canvas/9'])
g.add((c9, RDF.type, sc.Canvas))

# Add images on the canvases
g.add((c1, RDFS.label, StrLiteral('c1')))
g.add((c1, exif.height, Literal(4000, datatype=XSD.integer)))
g.add((c1, exif.width, Literal(3000, datatype=XSD.integer)))
g.add((c1, foaf.thumbnail, URIRef("http://localhost:8001/fcr/full/90,/0/default.jpg")))
(c1imgs, c1img) = ListStart(g, c1, sc.hasImageAnnotations)
g.add((c1img, RDF.type, oa.Annotation))
g.add((c1img, oa.motivatedBy, sc.painting))
c1img_svc = URIRef("http://localhost:8001/fcr")
c1img_full = URIRef("http://localhost:8001/fcr/full/full/0/default.jpg")
g.add((c1img, oa.hasBody, c1img_full))
g.add((c1img_full, RDF.type, dctypes.Image))
g.add((c1img_full, svcs.has_service, c1img_svc))
g.add((c1img_svc, doap.implements,
       URIRef("http://iiif.io/api/image/2/profiles/level0.json")))
g.add((c1img, oa.hasTarget, c1))

g.add((c2, RDFS.label, StrLiteral('c2')))
g.add((c2, exif.height, Literal(4000, datatype=XSD.integer)))
g.add((c2, exif.width, Literal(3000, datatype=XSD.integer)))
g.add((c2, foaf.thumbnail, URIRef("http://localhost:8001/fcv/full/90,/0/default.jpg")))
(c2imgs, c2img) = ListStart(g, c2, sc.hasImageAnnotations)
g.add((c2img, RDF.type, oa.Annotation))
# g.add((c2img2, oa.motivatedBy, sc.painting)) ## FIXME - framing fail
c2img_svc = URIRef("http://localhost:8001/fcv")
c2img_full = URIRef("http://localhost:8001/fcv/full/full/0/default.jpg")
g.add((c2img, oa.hasBody, c2img_full))
g.add((c2img_full, RDF.type, dctypes.Image))
g.add((c2img_full, svcs.has_service, c2img_svc))
# FIXME - framing failure, see hack later to replace
g.add((c2img_svc, doap.implements,
       URIRef("http://iiif.io/api/image/2/profiles/level0.json#c2")))
g.add((c2img, oa.hasTarget, c2))

g.add((c3, RDFS.label, StrLiteral('c3')))
g.add((c3, exif.height, Literal(4000, datatype=XSD.integer)))
g.add((c3, exif.width, Literal(3000, datatype=XSD.integer)))
g.add((c3, foaf.thumbnail, URIRef("http://localhost:8001/1r/full/90,/0/default.jpg")))
(c3imgs, c3img) = ListStart(g, c3, sc.hasImageAnnotations)
g.add((c3img, RDF.type, oa.Annotation))
# g.add((c3img2, oa.motivatedBy, sc.painting)) ## FIXME - framing fail
c3img_svc = URIRef("http://localhost:8001/1r")
c3img_full = URIRef("http://localhost:8001/1r/full/full/0/default.jpg")
g.add((c3img, oa.hasBody, c3img_full))
g.add((c3img_full, RDF.type, dctypes.Image))
g.add((c3img_full, svcs.has_service, c3img_svc))
# FIXME - framing failure, see hack later to replace
g.add((c3img_svc, doap.implements,
       URIRef("http://iiif.io/api/image/2/profiles/level0.json#c3")))
g.add((c3img, oa.hasTarget, c3))

g.add((c4, RDFS.label, StrLiteral('c4')))
g.add((c4, exif.height, Literal(4000, datatype=XSD.integer)))
g.add((c4, exif.width, Literal(3000, datatype=XSD.integer)))
g.add((c4, foaf.thumbnail, URIRef("http://localhost:8001/1v2r/full/90,/0/default.jpg")))
(c4imgs, c4img) = ListStart(g, c4, sc.hasImageAnnotations)
g.add((c4img, RDF.type, oa.Annotation))
# g.add((c4img2, oa.motivatedBy, sc.painting)) ## FIXME - framing fail
c4img_svc = URIRef("http://localhost:8001/1v2r")
c4img_full = URIRef("http://localhost:8001/1v2r/full/full/0/default.jpg")
g.add((c4img, oa.hasBody, c4img_full))
g.add((c4img_full, RDF.type, dctypes.Image))
g.add((c4img_full, svcs.has_service, c4img_svc))
# FIXME - framing failure, see hack later to replace
g.add((c4img_svc, doap.implements,
       URIRef("http://iiif.io/api/image/2/profiles/level0.json#c4")))
g.add((c4img, oa.hasTarget, c4))

g.add((c5, RDFS.label, StrLiteral('c5')))
g.add((c5, exif.height, Literal(4000, datatype=XSD.integer)))
g.add((c5, exif.width, Literal(3000, datatype=XSD.integer)))
g.add((c5, foaf.thumbnail, URIRef("http://localhost:8001/2v/full/90,/0/default.jpg")))
(c5imgs, c5img) = ListStart(g, c5, sc.hasImageAnnotations)
g.add((c5img, RDF.type, oa.Annotation))
# g.add((c5img2, oa.motivatedBy, sc.painting)) ## FIXME - framing fail
c5img_svc = URIRef("http://localhost:8001/2v")
c5img_full = URIRef("http://localhost:8001/2v/full/full/0/default.jpg")
g.add((c5img, oa.hasBody, c5img_full))
g.add((c5img_full, RDF.type, dctypes.Image))
g.add((c5img_full, svcs.has_service, c5img_svc))
# FIXME - framing failure, see hack later to replace
g.add((c5img_svc, doap.implements,
       URIRef("http://iiif.io/api/image/2/profiles/level0.json#c5")))
g.add((c5img, oa.hasTarget, c5))

g.add((c6, RDFS.label, StrLiteral('c6')))
g.add((c6, exif.height, Literal(4000, datatype=XSD.integer)))
g.add((c6, exif.width, Literal(3000, datatype=XSD.integer)))
g.add((c6, foaf.thumbnail, URIRef("http://localhost:8001/3r/full/90,/0/default.jpg")))
(c6imgs, c6img) = ListStart(g, c6, sc.hasImageAnnotations)
g.add((c6img, RDF.type, oa.Annotation))
# g.add((c6img2, oa.motivatedBy, sc.painting)) ## FIXME - framing fail
c6img_svc = URIRef("http://localhost:8001/3r")
c6img_full = URIRef("http://localhost:8001/3r/full/full/0/default.jpg")
g.add((c6img, oa.hasBody, c6img_full))
g.add((c6img_full, RDF.type, dctypes.Image))
g.add((c6img_full, svcs.has_service, c6img_svc))
# FIXME - framing failure, see hack later to replace
g.add((c6img_svc, doap.implements,
       URIRef("http://iiif.io/api/image/2/profiles/level0.json#c6")))
g.add((c6img, oa.hasTarget, c6))

g.add((c7, RDFS.label, StrLiteral('c7')))
g.add((c7, exif.height, Literal(4000, datatype=XSD.integer)))
g.add((c7, exif.width, Literal(3000, datatype=XSD.integer)))
g.add((c7, foaf.thumbnail, URIRef("http://localhost:8001/3v/full/90,/0/default.jpg")))
(c7imgs, c7img) = ListStart(g, c7, sc.hasImageAnnotations)
g.add((c7img, RDF.type, oa.Annotation))
# g.add((c7img2, oa.motivatedBy, sc.painting)) ## FIXME - framing fail
c7img_svc = URIRef("http://localhost:8001/3v")
c7img_full = URIRef("http://localhost:8001/3v/full/full/0/default.jpg")
g.add((c7img, oa.hasBody, c7img_full))
g.add((c7img_full, RDF.type, dctypes.Image))
g.add((c7img_full, svcs.has_service, c7img_svc))
# FIXME - framing failure, see hack later to replace
g.add((c7img_svc, doap.implements,
       URIRef("http://iiif.io/api/image/2/profiles/level0.json#c7")))
g.add((c7img, oa.hasTarget, c7))

g.add((c8, RDFS.label, StrLiteral('c8')))
g.add((c8, exif.height, Literal(4000, datatype=XSD.integer)))
g.add((c8, exif.width, Literal(3000, datatype=XSD.integer)))
g.add((c8, foaf.thumbnail, URIRef("http://localhost:8001/bcr/full/90,/0/default.jpg")))
(c8imgs, c8img) = ListStart(g, c8, sc.hasImageAnnotations)
g.add((c8img, RDF.type, oa.Annotation))
# g.add((c8img2, oa.motivatedBy, sc.painting)) ## FIXME - framing fail
c8img_svc = URIRef("http://localhost:8001/bcr")
c8img_full = URIRef("http://localhost:8001/bcr/full/full/0/default.jpg")
g.add((c8img, oa.hasBody, c8img_full))
g.add((c8img_full, RDF.type, dctypes.Image))
g.add((c8img_full, svcs.has_service, c8img_svc))
# FIXME - framing failure, see hack later to replace
g.add((c8img_svc, doap.implements,
       URIRef("http://iiif.io/api/image/2/profiles/level0.json#c8")))
g.add((c8img, oa.hasTarget, c8))

g.add((c9, RDFS.label, StrLiteral('c9')))
g.add((c9, exif.height, Literal(4000, datatype=XSD.integer)))
g.add((c9, exif.width, Literal(3000, datatype=XSD.integer)))
g.add((c9, foaf.thumbnail, URIRef("http://localhost:8001/bcv/full/90,/0/default.jpg")))
(c9imgs, c9img) = ListStart(g, c9, sc.hasImageAnnotations)
g.add((c9img, RDF.type, oa.Annotation))
# g.add((c9img2, oa.motivatedBy, sc.painting)) ## FIXME - framing fail
c9img_svc = URIRef("http://localhost:8001/bcv")
c9img_full = URIRef("http://localhost:8001/bcv/full/full/0/default.jpg")
g.add((c9img, oa.hasBody, c9img_full))
g.add((c9img_full, RDF.type, dctypes.Image))
g.add((c9img_full, svcs.has_service, c9img_svc))
# FIXME - framing failure, see hack later to replace
g.add((c9img_svc, doap.implements,
       URIRef("http://iiif.io/api/image/2/profiles/level0.json#c9")))
g.add((c9img, oa.hasTarget, c9))

# Get JSON-LD object in PyLD form
jld = pyld_json_from_rdflib_graph(g)

# Frame and compact...
framed = jsonld.compact(
    jsonld.frame(jld, "http://iiif.io/api/presentation/2/manifest_frame.json"),
    "http://iiif.io/api/presentation/2/context.json")
# FIXME - hack to get around framing problems
framed['sequences'][0]['canvases'][1]['images'][0]['resource']['service']['profile'] = "http://iiif.io/api/image/2/profiles/level0.json"
framed['sequences'][0]['canvases'][2]['images'][0]['resource']['service']['profile'] = "http://iiif.io/api/image/2/profiles/level0.json"
framed['sequences'][0]['canvases'][3]['images'][0]['resource']['service']['profile'] = "http://iiif.io/api/image/2/profiles/level0.json"
framed['sequences'][0]['canvases'][4]['images'][0]['resource']['service']['profile'] = "http://iiif.io/api/image/2/profiles/level0.json"
framed['sequences'][0]['canvases'][5]['images'][0]['resource']['service']['profile'] = "http://iiif.io/api/image/2/profiles/level0.json"
framed['sequences'][0]['canvases'][6]['images'][0]['resource']['service']['profile'] = "http://iiif.io/api/image/2/profiles/level0.json"
framed['sequences'][0]['canvases'][7]['images'][0]['resource']['service']['profile'] = "http://iiif.io/api/image/2/profiles/level0.json"
framed['sequences'][0]['canvases'][8]['images'][0]['resource']['service']['profile'] = "http://iiif.io/api/image/2/profiles/level0.json"
with open('jabberwocky/manifest.json', 'w') as fh:
    json.dump(framed, fh, indent=2, sort_keys=True)
