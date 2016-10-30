"""Make PyLD use cached documents (contexts, frames, etc.) if available."""

import logging
import os
import json
from pyld import jsonld

CACHE_DIR = os.path.normpath(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..', 'cache'))
CACHE_INDEX_FILENAME = 'index.json'
INDEX = {}


def index_cache():
    """Read index of cached JSON documents."""
    filename = os.path.join(CACHE_DIR, CACHE_INDEX_FILENAME)
    global INDEX
    INDEX = json.loads(open(filename, 'r').read())


def cached_load_document(url):
    """Read local cached copy of URL if available, else fallback to network."""
    if (url not in INDEX):
        logging.debug("Using default loader to get %s" % (url))
        return(jsonld.load_document(url))
    else:
        logging.debug("Reading %s from %s" % (url, INDEX[url]))
        data = open(os.path.join(CACHE_DIR, INDEX[url]), 'r').read()
        doc = {
            'contextUrl': None,
            'documentUrl': None,
            'document': data
        }
        return doc


# On load we read index and set up PyLD code
index_cache()
jsonld.set_document_loader(cached_load_document)
