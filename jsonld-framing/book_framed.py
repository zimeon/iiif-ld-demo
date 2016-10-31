"""Frame JSON-LD for to get Page objects based on typing."""
from pyld import jsonld
import json
import sys
doc = json.loads(open('book.json').read())
frame = json.loads(sys.argv[1] or "{}")
framed = jsonld.compact(jsonld.frame(doc, frame), {})
print(json.dumps(framed, indent=2, sort_keys=True))
