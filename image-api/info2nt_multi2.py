"""Parse info.json example with profile and sizes."""
from rdflib import Graph
import context_cache.for_rdflib_jsonld
info_json = """
{
  "@context" : "http://iiif.io/api/image/2/context.json",
  "@id" : "http://example.org/svc/id1",
  "protocol" : "http://iiif.io/api/image",
  "width" : 6000,
  "height" : 4000,
  "profile" : [
    "http://iiif.io/api/image/2/level2.json",
    "http://example.org/profile2"
  ],
  "sizes" : [ { "width": "150", "height": "100" } ]
}
"""
g = Graph().parse(data=info_json, format='json-ld')
print(g.serialize(format='nt').decode('utf-8'))
