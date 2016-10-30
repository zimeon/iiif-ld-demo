# Read Image API `info.json`

The [IIIF Image API](http://iiif.io/api/image/2.1/) specifies as JSON-LD document format for Image Information, called `info.json`. The document provides information required for a client to understand what image services are available for the given image. In addition to this technical metadata there may also be rights and licensing information. This is service/resource-based and not server-based: there is a separate `info.json` for every image.

The `info.json` document _MUST_ include a `@context` `<http://iiif.io/api/image/2/context.json>` and this specifies how to translate the simple JSON into RDF.

``` sh
image-api> python info2nt.py
```

``` json
Loading context  http://iiif.io/api/image/2/context.json
Loading context  http://iiif.io/api/annex/services/physdim/1/context.json
Loading context  http://geojson.org/contexts/geojson-base.jsonld
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://purl.org/dc/terms/rights> <http://example.org/rights/license1.html> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://purl.org/dc/terms/rights> <https://creativecommons.org/licenses/by/4.0/> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://iiif.io/api/image/2#hasSize> _:N66f4c16ca18841559e4535ca16c6ac05 .
_:N07e2b1b80c344da68103400a28b548b0 <http://iiif.io/api/image/2#format> "gif"^^<http://www.w3.org/2001/XMLSchema#string> .
_:N13025eec1442441588996d3709b8c479 <http://www.w3.org/2003/12/exif/ns#width> "3000"^^<http://www.w3.org/2001/XMLSchema#integer> .
_:N997690c222914bda9fb54ac97c981cdb <http://iiif.io/api/image/2#scaleFactor> "1"^^<http://www.w3.org/2001/XMLSchema#integer> .
_:N9df1c38dc9df489c9c25acb74b4828ab <http://www.w3.org/2003/12/exif/ns#height> "2048"^^<http://www.w3.org/2001/XMLSchema#integer> .
_:N07e2b1b80c344da68103400a28b548b0 <http://iiif.io/api/image/2#supports> <http://iiif.io/api/image/2#arbitraryRotationFeature> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://rdfs.org/sioc/services#has_service> <http://www.example.org/geojson/paris.json> .
_:N66f4c16ca18841559e4535ca16c6ac05 <http://www.w3.org/2003/12/exif/ns#width> "600"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://www.w3.org/2003/12/exif/ns#height> "4000"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://iiif.io/api/image/2#hasTile> _:N997690c222914bda9fb54ac97c981cdb .
_:N18d8488b3ffc4253930e775ac3bad35e <http://usefulinc.com/ns/doap#implements> <http://iiif.io/api/annex/services/physdim> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://www.w3.org/2003/12/exif/ns#width> "6000"^^<http://www.w3.org/2001/XMLSchema#integer> .
_:N54ebc41ae2964741baea46c758768f87 <http://www.w3.org/2003/12/exif/ns#height> "100"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://usefulinc.com/ns/doap#implements> <http://iiif.io/api/image/2/level2.json> .
_:N18d8488b3ffc4253930e775ac3bad35e <http://iiif.io/api/presentation/2#physicalUnits> "in"^^<http://www.w3.org/2001/XMLSchema#string> .
_:N07e2b1b80c344da68103400a28b548b0 <http://iiif.io/api/image/2#supports> <http://iiif.io/api/image/2#profileLinkHeaderFeature> .
_:N07e2b1b80c344da68103400a28b548b0 <http://iiif.io/api/image/2#supports> <http://example.com/feature/> .
_:N997690c222914bda9fb54ac97c981cdb <http://iiif.io/api/image/2#scaleFactor> "4"^^<http://www.w3.org/2001/XMLSchema#integer> .
_:N9df1c38dc9df489c9c25acb74b4828ab <http://iiif.io/api/image/2#scaleFactor> "16"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://iiif.io/api/image/2#hasTile> _:N9df1c38dc9df489c9c25acb74b4828ab .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://usefulinc.com/ns/doap#implements> _:N07e2b1b80c344da68103400a28b548b0 .
_:N13025eec1442441588996d3709b8c479 <http://www.w3.org/2003/12/exif/ns#height> "2000"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://example.org/image-service/logo/full/200,/0/default.png> <http://rdfs.org/sioc/services#has_service> <http://example.org/image-service/logo> .
_:N18d8488b3ffc4253930e775ac3bad35e <http://iiif.io/api/presentation/2#physicalScale> "0.0025"^^<http://www.w3.org/2001/XMLSchema#float> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://rdfs.org/sioc/services#has_service> _:N18d8488b3ffc4253930e775ac3bad35e .
_:N9df1c38dc9df489c9c25acb74b4828ab <http://iiif.io/api/image/2#scaleFactor> "8"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://iiif.io/api/presentation/2#attributionLabel> "<span>Darparwyd gan Enghraifft Sefydliad</span>"@cy .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://purl.org/dc/terms/conformsTo> <http://iiif.io/api/image> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://iiif.io/api/presentation/2#attributionLabel> "<span>Provided by Example Organization</span>"@en .
_:N07e2b1b80c344da68103400a28b548b0 <http://iiif.io/api/image/2#quality> "color"^^<http://www.w3.org/2001/XMLSchema#string> .
_:N07e2b1b80c344da68103400a28b548b0 <http://iiif.io/api/image/2#quality> "gray"^^<http://www.w3.org/2001/XMLSchema#string> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://iiif.io/api/image/2#hasSize> _:N54ebc41ae2964741baea46c758768f87 .
_:N07e2b1b80c344da68103400a28b548b0 <http://iiif.io/api/image/2#format> "pdf"^^<http://www.w3.org/2001/XMLSchema#string> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://iiif.io/api/image/2#hasSize> _:N13025eec1442441588996d3709b8c479 .
_:N66f4c16ca18841559e4535ca16c6ac05 <http://www.w3.org/2003/12/exif/ns#height> "400"^^<http://www.w3.org/2001/XMLSchema#integer> .
_:N9df1c38dc9df489c9c25acb74b4828ab <http://www.w3.org/2003/12/exif/ns#width> "1024"^^<http://www.w3.org/2001/XMLSchema#integer> .
_:N997690c222914bda9fb54ac97c981cdb <http://iiif.io/api/image/2#scaleFactor> "2"^^<http://www.w3.org/2001/XMLSchema#integer> .
_:N54ebc41ae2964741baea46c758768f87 <http://www.w3.org/2003/12/exif/ns#width> "150"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://example.org/image-service/logo> <http://usefulinc.com/ns/doap#implements> <http://iiif.io/api/image/2/level2.json> .
_:N997690c222914bda9fb54ac97c981cdb <http://www.w3.org/2003/12/exif/ns#width> "512"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C> <http://xmlns.com/foaf/0.1/logo> <http://example.org/image-service/logo/full/200,/0/default.png> .
_:N07e2b1b80c344da68103400a28b548b0 <http://iiif.io/api/image/2#supports> <http://iiif.io/api/image/2#canonicalLinkHeaderFeature> .
```
