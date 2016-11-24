"""Make rdflib_jsonld use cached documents (contexts, frames, etc.) if available."""

import logging
from rdflib.py3compat import PY3
from rdflib_jsonld import util
from rdflib.parser import create_input_source
if PY3:
    from io import StringIO
import json

from .local_cache import in_cache

def source_to_json_with_cache(source):
    # Based on rdflib.util.source_to_json
    filepath = in_cache(source)
    if (filepath is None):
        logging.debug("Using default loader to get %s" % (source))
        source = create_input_source(source, format='json-ld')
    else:
        logging.debug("Reading %s from %s" % (source, filepath))
        source = create_input_source(filepath, format='json-ld')

    stream = source.getByteStream()
    try:
        if PY3:
            return json.load(StringIO(stream.read().decode('utf-8')))
        else:
            return json.load(stream)
    finally:
        stream.close()

# On load set up rdflib code to use cached loader
util.source_to_json = source_to_json_with_cache
