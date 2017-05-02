"""Build IIIF Image API info.json from RDF, multiple profiles."""
from rdflib import Graph, URIRef, Literal, BNode, plugin
from rdflib.namespace import Namespace, XSD
from rdflib_jsonld.serializer import from_rdf

from rdflib_pyld_compat import pyld_jsonld_from_rdflib_graph

import json
from pyld import jsonld
import context_cache.for_pyld

# Namespaces used in IIIF Image API,
# see: http://iiif.io/api/image/2/context.json
iiif = Namespace("http://iiif.io/api/image/2#")
exif = Namespace("http://www.w3.org/2003/12/exif/ns#")
dc = Namespace("http://purl.org/dc/elements/1.1/")
dcterms = Namespace("http://purl.org/dc/terms/")
doap = Namespace("http://usefulinc.com/ns/doap#")
svcs = Namespace("http://rdfs.org/sioc/services#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
sc = Namespace("http://iiif.io/api/presentation/2#")

# Build graph with properties as described in
# http://iiif.io/api/image/2.1/#image-information-request
#
# A minimal valid info.json includes @context, @id, protocol,
# width, height and profile
g = Graph()
id = URIRef("http://example.org/prefix/id")
g.add((id, dcterms.conformsTo, URIRef("http://iiif.io/api/image")))
g.add((id, exif.width, Literal(4000, datatype=XSD.integer)))
g.add((id, exif.height, Literal(3000, datatype=XSD.integer)))
g.add((id, doap.implements, URIRef("http://example.org/profileA")))
g.add((id, doap.implements, URIRef("http://iiif.io/api/image/2/level0.json")))

info = pyld_jsonld_from_rdflib_graph(g)
framed = jsonld.compact(
    jsonld.frame(info, "http://iiif.io/api/image/2/info_frame.json"),
    "http://iiif.io/api/image/2/context.json")
framed = jsonld.compact(framed, "http://iiif.io/api/image/2/context.json")

print(json.dumps(framed, indent=2, sort_keys=True))
