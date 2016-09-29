"""Attempt to build IIIF Image API info.json from RDF.

I'm not sure why one would want to do this, but let us
see what can be done...
"""
from rdflib import Graph, URIRef, Literal, plugin
from rdflib.namespace import Namespace, XSD

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
context = "http://iiif.io/api/image/2/context.json"
g.add((id, dcterms.conformsTo, URIRef("http://iiif.io/api/image")))
g.add((id, exif.width, Literal(4000, datatype=XSD.integer)))
g.add((id, exif.height, Literal(3000, datatype=XSD.integer)))
g.add((id, doap.implements, URIRef("http://iiif.io/api/image/2/level0.json")))  # CANNOT SPECIFY AS LIST
print(g.serialize(format='json-ld', context=context, indent=4).decode('utf-8'))
