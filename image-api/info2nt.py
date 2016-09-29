"""Parse info.json from IIIF Image API spec."""
from rdflib import Graph
g = Graph().parse('spec_info.json', format='json-ld')
print(g.serialize(format='nt', indent=4).decode('utf-8'))
