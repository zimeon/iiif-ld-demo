# Creating a Manifest

The central document or response of the Presentation API is the [manifest](http://iiif.io/api/presentation/2.1/#manifest):

> _"The manifest response contains sufficient information for the client to initialize itself and begin to display something quickly to the user. The manifest resource represents a single object and any intellectual work or works embodied within that object. In particular it includes the descriptive, rights and linking information for the object. It then embeds the sequence(s) of canvases that should be rendered to the user."_ \[[Presentation API - Manifest](http://iiif.io/api/presentation/2.1/#manifest)]

## URI and preamble

The manifest must have a URI that dereferences to the JSON-LD document. In this example we'll prepare our description so that we can host the data on a local server on port 8000. The URI for the manifest will be `http://localhost:8000/jabberwocky/manifest`.

The first example program [`jabber1.py`](jabber1.py)

``` shell
prezi-api> python jabber1.py
```

specifies the manifest type (`sc:Manifest`) and then uses the combination of [`@context`](http://iiif.io/api/presentation/2/context.json) and [`frame`](http://iiif.io/api/presentation/2/manifest_frame.json) to produce the following output:

```
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "@id": "http://localhost:8000/jabberwocky/manifest",
  "@type": "sc:Manifest"
}
```

The line of code:

``` python
import context_cache.for_pyld
```

means that PyLD will use local cached copies of the context and manifest (in [`cache`](../cache), index in [`cache/index.json`](../cache/index.json)) instead of requesting them from their internet locations. If you have a network connection you should be able to comment this line with no effect (except execution speed).

## Descriptive information


## Sequence

At least one sequence must be included in a manifest and it represents the order of the parts of the work, each represented by a Canvas.