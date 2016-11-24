"""Example code to read and frame manifest.

Based on
http://iiif.io/api/annex/notes/jsonld/#sample-usage
"""
from pyld import jsonld
import json

import context_cache.pyld

# copy of http://iiif.io/api/presentation/2.1/example/fixtures/1/manifest.json
manifest_doc = open("manifest_fixture_1.json").read()
manifest = json.loads(manifest_doc)
print(json.dumps(jsonld.compact(
    jsonld.frame(manifest, "http://iiif.io/api/presentation/2/manifest_frame.json"),
    "http://iiif.io/api/presentation/2/context.json"),
    indent=2, sort_keys=True))
