"""Make PyLD use cached documents (contexts, frames, etc.) if available."""

import logging
from pyld import jsonld

from .local_cache import in_cache


def cached_load_document(url):
    """Read local cached copy of URL if available, else fallback to network."""
    filepath = in_cache(url)
    if (filepath is None):
        logging.debug("Using default loader to get %s" % (url))
        return(jsonld.load_document(url))
    else:
        logging.debug("Reading %s from %s" % (url, filepath))
        data = open(filepath, 'r').read()
        doc = {
            'contextUrl': None,
            'documentUrl': None,
            'document': data
        }
        return doc


# On load set up PyLD code to use cached loader
jsonld.set_document_loader(cached_load_document)
