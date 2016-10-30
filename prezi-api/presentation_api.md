# IIIF Presentation API

The IIIF [Presentation API](http://iiif.io/api/presentation/), currently v2.1, uses the same sort of JSON-LD approach as the [Image API](http://iiif.io/api/image/), but has a number of documents that can be rather more complex.

The [JSON-LD Implementation Notes](http://iiif.io/api/annex/notes/jsonld/) include example code to frame a test fixture: <http://iiif.io/api/annex/notes/jsonld/#sample-usage>. We can run a version of this modified for py2/py3 support:

``` shell
prezi-api> python prezi_frame1.py 
```

which produces the following JSON-LD output:

``` json
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "@id": "http://iiif.io/api/presentation/2.0/example/fixtures/1/manifest.json",
  "@type": "sc:Manifest",
  "label": "Test 1 Manifest: Minimum Required Fields",
  "sequences": [
    {
      "@id": "_:b0",
      "@type": "sc:Sequence",
      "canvases": [
        {
          "@id": "http://iiif.io/api/presentation/2.0/example/fixtures/canvas/1/c1.json",
          "@type": "sc:Canvas",
          "height": 1800,
          "images": [
            {
              "@id": "_:b1",
              "@type": "oa:Annotation",
              "motivation": "sc:painting",
              "on": "http://iiif.io/api/presentation/2.0/example/fixtures/canvas/1/c1.json",
              "resource": {
                "@id": "http://iiif.io/api/presentation/2.0/example/fixtures/resources/page1-full.png",
                "@type": "dctypes:Image",
                "height": 1800,
                "width": 1200
              }
            }
          ],
          "label": "Test 1 Canvas: 1",
          "width": 1200
        }
      ]
    }
  ],
  "within": "http://iiif.io/api/presentation/2.0/example/fixtures/collection.json"
}
```
