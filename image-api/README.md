# IIIF Image API

> _"The IIIF Image API specifies a web service that returns an image in response to a standard HTTP or HTTPS request. The URI can specify the region, size, rotation, quality characteristics and format of the requested image. A URI can also be constructed to request basic technical information about the image to support client applications. This API was conceived of to facilitate systematic reuse of image resources in digital image repositories maintained by cultural heritage organizations. It could be adopted by any image repository or service, and can be used to retrieve static images in response to a properly constructed URI."_ \[[IIIF Image API - Introduction](http://iiif.io/api/image/2.1/#introduction)]

  * Slides: **[IIIF Image API (2.0)](http://www.slideshare.net/simeonwarner/iiif-image-api-ghent)** (released 2014-09-11)
  * [Non-breaking changes in IIIF Image API 2.1](http://iiif.io/api/image/2.1/change-log/) (released 2016-05-12)

## Image API Image Information as Linked Data / RDF

The [IIIF Image API](http://iiif.io/api/image/2.1/) specifies a JSON-LD document format for Image Information, called `info.json`. This document provides information required for a client to understand what image services are available for the given image. In addition to this technical metadata there may also be rights and licensing information. This is service/resource-based and not server-based: there is a separate `info.json` for every image.

All responses from the Image API other than the `info.json` are either image data or HTTP error codes.

  * [Reading Image API Image Information as RDF](read_image_info.md)
  * [Writing Image API Image Information from RDF](write_image_info.md)

---

_| [Index](../README.md) | [Next: IIIF Presentation API](../prezi_api/README.md) |_