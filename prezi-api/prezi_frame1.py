"""Example code to read and frame manifest.

Based on
http://iiif.io/api/annex/notes/jsonld/#sample-usage
"""
from pyld.jsonld import compact, frame
import urllib
import json
try:
    from urllib.request import urlopen
except ImportError:  # py2
    from urllib import urlopen

import pyld_local_cache

# copy of http://iiif.io/api/presentation/2.1/example/fixtures/1/manifest.json
manifest_doc = open("manifest_fixture_1.json").read()
manifest = json.loads(manifest_doc)
print(json.dumps(compact(
    frame(manifest, "http://iiif.io/api/presentation/2/manifest_frame.json"),
    "http://iiif.io/api/presentation/2/context.json"),
    indent=2, sort_keys=True))
