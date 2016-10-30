"""Parse info.json from IIIF Image API spec."""
import os, sys
os.chdir(sys.path[0])

from rdflib import Graph
g = Graph().parse('spec_info.json', format='json-ld')
print(g.serialize(format='nt').decode('utf-8'))
