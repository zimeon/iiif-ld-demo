"""Attempt to build IIIF Image API info.json from RDF.

I'm not sure why one would want to do this, but let us
see what can be done...
"""
from rdflib import Graph, URIRef, Literal, BNode, plugin
from rdflib.namespace import Namespace, XSD

from rdflib_jsonld.serializer import from_rdf
import json
import sys


def serialize_as_jsonld(graph, stream, base=None, encoding=None, **kwargs):
    """Serialize RDF graph as JSONLD.

    Code copied from:
    https://github.com/RDFLib/rdflib-jsonld/blob/master/rdflib_jsonld/serializer.py
    with addition of json_hook functionality.
    """
    # TODO: docstring w. args and return value
    encoding = encoding or 'utf-8'
    if encoding not in ('utf-8', 'utf-16'):
        warnings.warn("JSON should be encoded as unicode. " +
                      "Given encoding was: %s" % encoding)

    context_data = kwargs.get('context')
    use_native_types = kwargs.get('use_native_types', False),
    use_rdf_type = kwargs.get('use_rdf_type', False)
    auto_compact = kwargs.get('auto_compact', False)

    indent = kwargs.get('indent', 2)
    separators = kwargs.get('separators', (',', ': '))
    sort_keys = kwargs.get('sort_keys', True)
    ensure_ascii = kwargs.get('ensure_ascii', False)

    obj = from_rdf(graph.store, context_data, base,
                   use_native_types, use_rdf_type,
                   auto_compact=auto_compact)

    # Check hook for JSON postprocessing
    json_hook = kwargs.get('json_hook', None)
    if (json_hook is not None):
        obj = json_hook(obj)

    data = json.dumps(obj, indent=indent, separators=separators,
                      sort_keys=sort_keys, ensure_ascii=ensure_ascii)
    return data
    # stream.write(data.encode(encoding, 'replace'))


def iiifize_image_api_jsonld(obj):
    """Modify plain JSONLD to be IIIF compliant JSONLD."""
    obj['@context'] = "http://iiif.io/api/image/2/context.json"
    if ('profile' in obj):
        obj['profile'] = [obj['profile']]
    return(obj)


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
# context = "http://iiif.io/api/image/2/context.json"
context = "image-api/context.json"
g.add((id, dcterms.conformsTo, URIRef("http://iiif.io/api/image")))
g.add((id, exif.width, Literal(4000, datatype=XSD.integer)))
g.add((id, exif.height, Literal(3000, datatype=XSD.integer)))
g.add((id, doap.implements, URIRef("http://iiif.io/api/image/2/level0.json")))  # CANNOT SPECIFY AS LIST
g.add((id, sc.attributionLabel, Literal(
    "<span>Provided by Example Organization</span>",
    lang="en")))
g.add((id, sc.attributionLabel, Literal(
    "<span>Darparwyd gan Enghraifft Sefydliad</span>",
    lang="cy")))

logo = URIRef("http://example.org/image-service/logo/full/200,/0/default.png")
g.add((id, foaf.logo, logo))
# # If the logo service is added this will cause the serialization
# # to use @graph
# logo_svc = URIRef("http://example.org/image-service/logo")
# g.add((logo, svcs.has_service, logo_svc))
# ??g.add((logo_svc, "@context", URIRef("http://iiif.io/api/image/2/context.json")))
# g.add((logo_svc, doap.implements, URIRef("http://iiif.io/api/image/2/level2.json")))


#  "license" : [
#    "http://example.org/rights/license1.html",
#    "https://creativecommons.org/licenses/by/4.0/"
#  ],
#  "profile" : [
#    "http://iiif.io/api/image/2/level2.json",
#    {
#      "formats" : [ "gif", "pdf" ],
#      "qualities" : [ "color", "gray" ],
#      "supports" : [
#        "canonicalLinkHeader", "rotationArbitrary", "profileLinkHeader", "http://example.com/feature/"
#      ]
#    }
#  ],
#  "service" : [
#    {
#      "@context": "http://iiif.io/api/annex/service/physdim/1/context.json",
#      "profile": "http://iiif.io/api/annex/service/physdim",
#      "physicalScale": 0.0025,
#      "physicalUnits": "in"
#    },{
#      "@context" : "http://geojson.org/contexts/geojson-base.jsonld",
#      "@id" : "http://www.example.org/geojson/paris.json"
#    }
#  ]

# The following simply does not work:
size1 = BNode()
g.add((id, iiif.hasSize, size1))
g.add((size1, exif.width, Literal(400, datatype=XSD.integer)))
g.add((size1, exif.height, Literal(300, datatype=XSD.integer)))
tile1 = BNode()
g.add((id, iiif.hasTile, tile1))
g.add((tile1, exif.width, Literal(512, datatype=XSD.integer)))
g.add((tile1, iiif.scaleFactor, Literal(1, datatype=XSD.integer)))
g.add((tile1, iiif.scaleFactor, Literal(2, datatype=XSD.integer)))
g.add((tile1, iiif.scaleFactor, Literal(4, datatype=XSD.integer)))


print(serialize_as_jsonld(g, sys.stdout, format='json-ld', context=context, json_hook=iiifize_image_api_jsonld, indent=2))
