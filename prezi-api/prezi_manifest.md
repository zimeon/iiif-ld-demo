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

``` json
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

It is important to note that the descriptive information included in the manifest is intended simply for display to the user, it is not a place for structured semantic bibliographic or other metadata (that can be linked to with `seeAlso`).

In the [`second program`](jabber2.py) we add a `label`, a `description`, and a tagged `Author` field:

``` shell
prezi-api> python jabber2.py
```

but here the output is wrong, we have a single `sc:metadataLabels` object where we want to have a `metadata` property with a list of `label`/`value` pairs:

``` json
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "@id": "http://localhost:8000/jabberwocky/manifest",
  "@type": "sc:Manifest",
  "description": "A bad edition of wonderful nonsense.",
  "label": "Jabberwocky",
  "sc:metadataLabels": {
    "@id": "_:b0",
    "label": "Author",
    "value": "Lewis Carroll"
  }
}
```

The problem here is that the `sc:metadataLabels` RDF resource must be and [`RDF:List`](https://www.w3.org/TR/rdf-schema/#ch_list) of `label`/`value` pairs. We can fix this in a [third program](jabber3.py):

``` shell
prezi-api> python jabber3.py
```

which adds a second pair and produces the correct structure:

``` json
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "@id": "http://localhost:8000/jabberwocky/manifest",
  "@type": "sc:Manifest",
  "description": "A bad edition of wonderful nonsense.",
  "label": "Jabberwocky",
  "metadata": [
    {
      "@id": "_:b1",
      "label": "Author",
      "value": "Lewis Carroll"
    },
    {
      "@id": "_:b0",
      "label": "Published",
      "value": "1871"
    }
  ]
}
```

## Sequence and canvases

At least one sequence must be included in a manifest and it represents the order of the parts of the work, each represented by a canvas. As a first stab we add a single sequence and then two canveses (with no content). The functions `ListStart` and `ListAdd` are defined to make list creation a little simpler.

``` shell
prezi-api> python jabber4.py
```

produces:

``` json
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "@id": "http://localhost:8000/jabberwocky/manifest",
  "@type": "sc:Manifest",
  "description": "A bad edition of wonderful nonsense.",
  "label": "Jabberwocky",
  "metadata": [
    {
      "@id": "_:b4",
      "label": "Author",
      "value": "Lewis Carroll"
    },
    {
      "@id": "_:b1",
      "label": "Published",
      "value": "1871"
    }
  ],
  "sequences": [
    {
      "@id": "_:b2",
      "@type": "sc:Sequence",
      "canvases": [
        {
          "@id": "_:b3",
          "@type": "sc:Canvas"
        },
        {
          "@id": "_:b0",
          "@type": "sc:Canvas"
        }
      ],
      "label": "Normal Page Order"
    }
  ]
}
```

To load with test server running on <http://localhost:8000/>:

  * [UV](http://universalviewer.io/?manifest=http%3A%2F%2Flocalhost%3A8000%2Fjabberwocky%2Fmanifest.json)
  * [Mirador](http://projectmirador.org/demo/) then "Replace Object" and enter `http://localhost:8000/jabberwocky/manifest.json` into Load box.

---

_| [Up](README.md) |_
