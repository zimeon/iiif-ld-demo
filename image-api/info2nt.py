"""Parse info.json from IIIF Image API spec."""
import os
import sys
from rdflib import Graph
os.chdir(sys.path[0])

g = Graph().parse('spec_info.json', format='json-ld')
print(g.serialize(format='nt').decode('utf-8'))
