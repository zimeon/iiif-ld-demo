from rdflib import Graph, plugin
g = Graph().parse('spec_info.json', format='json-ld')
print(g.serialize(format='nt', indent=4))
