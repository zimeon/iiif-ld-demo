"""Use @context to convert RDF to JSON-LD."""
from rdflib import Graph
import context_cache.rdflib_jsonld

g = Graph().parse(format="nt", data="""
<http://zimeon.com/me> <http://schema.org/gender> "Male" .
<http://zimeon.com/me> <http://schema.org/honorificPrefix> "Dr" .
<http://zimeon.com/me> <http://xmlns.com/foaf/0.1/familyName> "Warner" .
<http://zimeon.com/me> <http://xmlns.com/foaf/0.1/givenName> "Simeon" .
<http://zimeon.com/me> <http://xmlns.com/foaf/0.1/name> "Simeon Warner" .
<http://zimeon.com/me> <http://xmlns.com/foaf/0.1/title> "Lesser Pooh-Bah" .
""")

print(g.serialize(format='json-ld',
                  context="http://json-ld.org/contexts/person.jsonld",
                  indent=2).decode('utf-8'))
