# Writing IIIF Image API `info.json`

I'm really not sure why one would want to write an IIIF Image API `info.json` from RDF data, but let's explore it as an academic exercise.

The `@context` doesn't support seamless creation of IIIF Image API `info.json` from RDF. There is one instance where the output of straight conversion to JSON-LD will not have the complete semantics, and IIIF-aware serializer is necessary to conform the the specification:

  * Image API `profile` is a list where order in regard to the first element is significant but this is not expressed in the `@context` (see <https://github.com/IIIF/iiif.io/blob/master/source/api/image/2/context.json#L121-L124>). If one `profile` value is given, it will appear in straight conversion as a value and note a single entry list. If multipe `profile` values are given, they will appear as an unsorted list whereas the Image API specification requires that the compliance level profile be the first entry.

It is merely convention, and not a requirement of the specification, that properties such as `sizes` and `tiles` typically appear in size order. Clients should not rely on this ordering.

## A minimal `info.json`

The first program:

``` shell
image-api> python build_image_info_frame1.py 
```

produces an **invalid** Image Information (`info.json`):


``` json
{
  "@context": "http://iiif.io/api/image/2/context.json",
  "@id": "http://example.org/prefix/id",
  "height": "3000",
  "profile": "http://iiif.io/api/image/2/level0.json",
  "protocol": "http://iiif.io/api/image",
  "width": "4000"
}
```

It is invalid because the `profile` should be a list, and not a single URI.


``` sh
image-api>python build_image_info_frame2.py 
```

will produce output that when run repeatedly vaires the order of the two entries in `profile`:

``` json
...
  "profile": [
    "http://example.org/profileB",
    "http://iiif.io/api/image/2/level0.json"
  ],
...
```

``` shell
image-api> diff build_image_info_frame2.py  build_image_info_frame3.py 
```

``` python
41a42,55
> if ('profile' in framed):
>     # Fix-up `profile` to be a list
>     if (isinstance(framed['profile'], str)):
>         framed['profile'] = [framed['profile']]
>     # Fix-up `profile` list to have IIIF compliance URI first
>     if (len(framed['profile']) > 1):
>         profiles = []
>         for profile in framed['profile']:
>             if (profile.startswith('http://iiif.io/api/image/')):
>                 profiles.insert(0, profile)
>             else:
>                 profiles.append(profile)
>         framed['profile'] = profiles
> 
```

With this change, the following command

``` shell
image-api> python build_image_info_frame3.py 
```

will always produce the correct `profile` form, a list with the compliance level URI as the first entry:

``` json
{
  "@context": "http://iiif.io/api/image/2/context.json",
  "@id": "http://example.org/prefix/id",
  "height": "3000",
  "profile": [
    "http://iiif.io/api/image/2/level0.json",
    "http://example.org/profileA"
  ],
  "protocol": "http://iiif.io/api/image",
  "width": "4000"
}
```
