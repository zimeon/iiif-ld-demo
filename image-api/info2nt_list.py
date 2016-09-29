from rdflib import Graph
info_json = """
{
  "@context" : "context.json",
  "@id" : "http://example.org/svc/id1",
  "protocol" : "http://iiif.io/api/image",
  "width" : 6000,
  "height" : 4000,
  "profile" : [
    "http://iiif.io/api/image/2/level2.json",
    "http://example.org/profile2"
  ]
}
"""
g = Graph().parse(data=info_json, format='json-ld')
print(g.serialize(format='nt', indent=4).decode('utf-8'))

