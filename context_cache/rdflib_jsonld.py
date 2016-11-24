"""Make rdflib_jsonld use cached documents (contexts, frames, etc.) if available."""

import logging
from rdflib.py3compat import PY3
from rdflib_jsonld import util
from rdflib.parser import create_input_source
import json
from .local_cache import in_cache
if PY3:
    from io import StringIO

# Store reference to orginal function so we can wrap it
original_source_to_json = util.source_to_json


def source_to_json_with_cache(source):
    """Look for local cached version of source, else fallback to loading."""
    filepath = in_cache(source)
    if (filepath is None):
        logging.debug("Using default loader to get %s" % (source))
    else:
        logging.debug("Reading %s from %s" % (source, filepath))
        source = filepath
    return original_source_to_json(source)


# On load set up rdflib code to use loader with cache
util.source_to_json = source_to_json_with_cache
