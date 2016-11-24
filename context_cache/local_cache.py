"""Local cache of documents (contexts, frames, etc.)."""

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


def in_cache(url):
    """Return path if url in cache, else None."""
    if (url not in INDEX):
        return(None)
    else:
        return(os.path.join(CACHE_DIR, INDEX[url]))


# On load we read index
index_cache()
