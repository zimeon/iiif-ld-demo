# Writing IIIF Image API `info.json`

I'm really not sure why one would want to write an IIIF Image API `info.json` from RDF data, but let's explore it as an academic exercise.

The `@context` doesn't support seamless creation of IIIF Image API `info.json` from RDF. There are instances where the output of straight conversion to JSON-LD will not have the complete semantics, and IIIF-aware serializer is necessary to recover these correctly in the following cases:

  * Image API `profile` is a list where order is significant but this is not expressed in the `@context` (see <https://github.com/IIIF/iiif.io/blob/master/source/api/image/2/context.json#L121-L124>). If one `profile` value is given, it will appear in straight conversion as a value and note a single entry list. If multipe `profile` values are given, they will appear as an unsorted list whereas the Image API specification requires that the compliance level profile be the first entry.
  * FIXME ...
