# IIIF and Linked Data

_The principles of [Linked Data](http://linkeddata.org/) and the [Architecture of the Web](http://www.w3.org/TR/webarch/) are adopted in order to provide a distributed and interoperable system. The [Shared Canvas data model](http://iiif.io/model/shared-canvas/1.0) and [JSON-LD](http://www.w3.org/TR/json-ld/) are leveraged to create an easy-to-implement, JSON-based format._ \[[Presentation API Introduction](http://iiif.io/api/presentation/2.1/)]

## Architecture of the Web

All IIIF work assumes that content and descriptions live on the web, as web resources with URIs.

  * Distribution is assumed, co-location of resources on one server is not required or assumed. 
  * Convention is minimized in favor explicit hypertext approaches where that is tractable. For example, the [paging in the Content Search API](http://iiif.io/api/search/1.0/#paging-results) uses complete URIs instead of numbers and URI templates. Exceptions include the [Image API URI structure](http://iiif.io/api/image/#image-request-uri-syntax) and [Content Search API query parameters](http://iiif.io/api/search/#request), in both cases there are description documents which identify the specification/profile that the API implements and thus allow clients to generate appropriate requests.
  * The specifications leverage standard HTTP verbs (RESTful though currently read-only pending work on a REST specification), HTTP response codes, media types, and link headers.
  * Care has been taken to work well with web caching infrastructure (e.g. different URIs for high-quality and degraded content accessible with different authorizations).

## Linked Data

Going back to Tim Berners Lee in 2006:

> Like the web of hypertext, the web of data is constructed with documents on the web. However,  unlike the web of hypertext,  where links are relationships anchors in hypertext documents written in HTML, for data they links  between arbitrary things described by RDF,.  The URIs identify any kind of object or  concept.   But for HTML or RDF, the same expectations apply to make the web grow:
>   * Use URIs as names for things
>   * Use HTTP URIs so that people can look up those names.
>   * When someone looks up a URI, provide useful information, using the standards (RDF*, SPARQL)
>   * Include links to other URIs. so that they can discover more thing

  * URIs as names/identifiers per Architecture of the Web
  * HTTP URIs which resolve used, redirects for URIs that identify non-information resources / real-world objects (whichever term you prefer).
  * Information expressed as JSON-LD, a format of RDF (more later). No requirement to use SPARQL as we do not want to tie to a particular technology stack and the complexity/performance issues of triplestores.
  * Linking within objects fundamental to IIIF. Linking between objects supported via a set of aggregate structures in the [Presenation API](http://iiif.io/api/presentation/#additional-types) and additional methods being discussed to support discovery (e.g. ResourceSync, Sitemaps).
  * Ideally, all IIIF resources would be **Linked _Open_ Data**, but this will not always be possible. Everything works best and most conveniently when open. The [Authentication API](http://iiif.io/api/auth) provides ways to leverage (multiple) auth systems in a distributed environment, and to combine restricted access content and open content.

## Shared Canvas Data Model

The [Shared Canvas data model](http://iiif.io/model/shared-canvas/1.0) is the basis of the [Presenation API](http://iiif.io/api/presentation/). 

  * Abstract data model based on RDF, does not specify particular serialization formats or interaction patterns. 
  * Introduces notion of a canvas as _"a two dimensional rectangular space with an aspect ratio that represents a single logical view of some part of the physical item"_. The canvas is separately identified from any image or the physical page.
  * Images (and other information) are _annotated_ onto the canvas.
  * Annotations follow the [Open Annotation Data Model](http://www.openannotation.org/spec/core/).

## Annotations

The foundation of the [Open Annotation Data Model](http://www.openannotation.org/spec/core/) is the notion of an annotation resource that ties the body of an annotation to the thing it is about, the target. There is an _implied_ relation between the annotation body and the target.

![from Open Annotation: Figure 0.1. Annotation, Body and Target](oa_intro_model.png)

Within the Shared Canvas data modal and the IIIF Presentation API, a key use of annotation is to _paint_ images onto the _canvas_. The body of the annotation is the image, and the target of the annotation is the canvas. The body and target are typed, and the annotation itself has a _motivation_ `sc:painting` (this distinguishes it from comment annotations about the canvas, etc.).

![from Shared Canvas: Figure 3.1. Basic Annotation Model](sc_anno1.png)

The Presentation API also describes the use of annotations for transcription (also using `sc:painting` motivation, typically implemented using [Layers](http://iiif.io/api/presentation/#layer)), [commentary](http://iiif.io/api/presentation/#comment-annotations) (using `oa:commentation` motivation), and [hotspot linking](http://iiif.io/api/presentation/#hotspot-linking) (using `oa:linking` motivations). Of course, annatations with other established and new motivations may be used aswell.

**Slight change coming** -- The [Open Annotation Data Model](http://www.openannotation.org/spec/core/) data model (2013, W3C Community Draft) has been superseded by the [Web Annotation Data Model](https://www.w3.org/TR/annotation-model/), a W3C Candidate Recommendation expected to become a Recommendation soon (final standard status from W3C). We intend to update Shared Canvas (see [#496](https://github.com/IIIF/iiif.io/issues/496), [#719](https://github.com/IIIF/iiif.io/issues/719) and then the Presentation API (v3.0) -- there will be work on this in 2017.

## JSON-LD

> _"JSON-LD is a lightweight Linked Data format. It is easy for humans to read and write. It is based on the already successful JSON format and provides a way to help JSON data interoperate at Web-scale. JSON-LD is an ideal data format for programming environments, REST Web services, and unstructured databases such as CouchDB and MongoDB."_ \[[json-ld.org](http://json-ld.org/)]

Usability and smooth extension from plain JSON are key. You'll notice that this summary doesn't mention RDF directly. I think that is no accident because, while the JSON-LD community is composed of linked data and RDF beleivers, they have a focus on practical issues and work hard to avoid the real or perceived complexity and performance issues associated with RDF and the Semantic Web.

The JSON-LD specification does describe the close relationship between JSON-LD and RDF:

> _"JSON-LD is a [concrete RDF syntax](https://www.w3.org/TR/rdf11-concepts/#dfn-concrete-rdf-syntax) as described in \[[RDF11-CONCEPTS](https://www.w3.org/TR/rdf11-concepts/)\]. Hence, a JSON-LD document is both an RDF document and a JSON document and correspondingly represents an instance of an RDF data model. However, JSON-LD also extends the RDF data model to optionally allow JSON-LD to serialize [generalized RDF Datasets](http://www.w3.org/TR/rdf11-concepts/#dfn-generalized-rdf-dataset). The JSON-LD extensions to the RDF data model are:
> 
>  * In JSON-LD properties can be IRIs or blank nodes whereas in RDF properties (predicates) have to be IRIs. This means that JSON-LD serializes generalized RDF Datasets.
>  * In JSON-LD lists are part of the data model whereas in RDF they are part of a vocabulary, namely \[[RDF-SCHEMA](https://www.w3.org/TR/rdf-schema/)].
>  * RDF values are either typed literals (typed values) or language-tagged strings whereas JSON-LD also supports JSON's native data types, i.e., number, strings, and the boolean values true and false. The JSON-LD Processing Algorithms and API specification \[[JSON-LD-API](http://json-ld.org/spec/latest/json-ld/)] defines the conversion rules between JSON's native data types and RDF's counterparts to allow round-tripping.
> 
> Summarized, these differences mean that JSON-LD is capable of serializing any RDF graph or dataset and most, but not all, JSON-LD documents can be directly interpreted as RDF as described in RDF 1.1 Concepts \[[RDF11-CONCEPTS](https://www.w3.org/TR/rdf11-concepts/)\]."_ \[[ - Relationship to RDF](http://json-ld.org/spec/latest/json-ld/#relationship-to-rdf)\

The use of JSON-LD by all IIIF specifications means that all data exposed through them can trivially be used in RDF systems. It also means that RDF systems _should_ readily be able to be used to generate IIIF compatible description documents. Use as RDF depends on the JSON-LD `@context`, and generation from RDF systems depends on both the JSON-LD `@context` and _framing_ (discussed [later](jsonld-framing/index.md)).

### JSON-LD `@context`: Mapping plain JSON to RDF

The [JSON-LD Playground](http://json-ld.org/playground/) is an extremely useful tool for exploring and checking JSON-LD operations and understanding. It is a web tool based on the JavaScript reference implementation of a [JSON-LD processor](https://github.com/digitalbazaar/jsonld.js).

Let's consider some very simple JSON:

``` json
{ "name": "Simeon" }
```

we might think of this in RDF as a predicate `name` and an object `Simeon` - two-thirds of a triple. In JSON-LD the special `@id` keyword is used to identify nodes. Here we can add it to complete the "triple":

``` json
{ "@id": "http://zimeon.com/me",
  "name": "Simeon" }
```

But this is still meaningless because `name` isn't a valid predicate (you can test this by pasting into the [JSON-LD Playground](http://json-ld.org/playground/) and then selecting the "N-Quads" tab below. We can fix that by adding a `@context` to map `name` to a predicate IRI.

``` json
{ "@context": { "name": "http://xmlns.com/foaf/0.1/name" },
  "@id": "http://zimeon.com/me",
  "name": "Simeon" }
```

The above in interpretted correctly as the triple:

``` ntriples
<http://zimeon.com/me> <http://xmlns.com/foaf/0.1/name> "Simeon" .
```

(Don't worry about the fact that the playground tab is labelled "N-Quads", triples in the default graph are represented identically to ntriples output (see [N-Quads spec](https://www.w3.org/TR/n-quads/#simple-triples)). The IIIF specifications do no make use of named graphs.)

In the above we supplied the `@context` inline. It can alternatively be specified by reference. In the example below we use a context on the `json-ld.org` site, which includes the same definition of `name`. Hence, the JSON-LD:

``` json
{ "@context": "http://json-ld.org/contexts/person.jsonld",
  "@id": "http://zimeon.com/me",
  "name": "Simeon" }
```

is interpretted as the same triple:

``` ntriples
<http://zimeon.com/me> <http://xmlns.com/foaf/0.1/name> "Simeon" .
```

Finally, we could do the same thing without a context, by simply putting in the predicate IRI directly:

``` json
{
  "@id": "http://zimeon.com/me",
  "http://xmlns.com/foaf/0.1/name": "Simeon"
}
```

However, in this we lost the nice `name` JSON key. Perhaps in this minimal example it looks simpler but imagine a more complex description where the use of simple/clean JSON keys nicely hides the complexity of IRIs:

``` json
{
  "@context": "http://json-ld.org/contexts/person.jsonld",
  "@id": "http://zimeon.com/me",
  "name": "Simeon Warner",
  "givenName": "Simeon",
  "familyName": "Warner",
  "gender": "Male",
  "honorificPrefix": "Dr",
  "jobTitle": "Lesser Pooh-Bah"
}
```

The above translates to the following RDF ntriples:

``` ntriples
<http://zimeon.com/me> <http://schema.org/gender> "Male" .
<http://zimeon.com/me> <http://schema.org/honorificPrefix> "Dr" .
<http://zimeon.com/me> <http://xmlns.com/foaf/0.1/familyName> "Warner" .
<http://zimeon.com/me> <http://xmlns.com/foaf/0.1/givenName> "Simeon" .
<http://zimeon.com/me> <http://xmlns.com/foaf/0.1/name> "Simeon Warner" .
<http://zimeon.com/me> <http://xmlns.com/foaf/0.1/title> "Lesser Pooh-Bah" .
```

The `@context` also allows formatting of JSON-LD using nice property names based on RDF input. Such operations aren't supported in the JSON-LD Playground but instead we can write a simple Python [program](rdf_to_jsonld1.py) to demonstrate this. For example:

``` shell 
iiif_ld> python rdf_to_jsonld1.py
```

which includes the above RDF ntriples, and uses the context to produce:

``` json
{
  "@context": "http://json-ld.org/contexts/person.jsonld",
  "@id": "http://zimeon.com/me",
  "familyName": "Warner",
  "gender": "Male",
  "givenName": "Simeon",
  "honorificPrefix": "Dr",
  "jobTitle": "Lesser Pooh-Bah",
  "name": "Simeon Warner"
}
```

**FIXME** - add typing, prefixes, nesting, @context for RDF -> JSON-LD

Further reading on JSON-LD:

  * [JSON-LD: JSON for Linked Data](http://www.slideshare.net/gkellogg1/json-for-linked-data) - a presentation by Gregg Kellogg
  * [JSON-LD specification](http://json-ld.org/spec/latest/json-ld/) - quite readable as specifications go. Great to be able to plug many examples into the playground.
  * [Other JSON-LD Learning Resources](http://json-ld.org/learn.html).

**Minor change coming** -- There is an emerging best practice to use `id` and `type` in JSON-LD documents instead of `@id` and `@type` (via redefinition in the `@context`). This has already been done or agreed for other specifications (including [Web Annotation](https://www.w3.org/TR/annotation-model/#annotations)). The IIIF specifications currently use `@id` and `@type` but [will change](https://github.com/IIIF/iiif.io/issues/590), likely with version 3.0 of the Image and Presentation APIs.

## Why RDF if developers don't know/use it?

So far there are very little work around IIIF that uses an RDF stack. There is an obvious benefit of using RDF that it is compatible with systems based on this data model, although there are still opportunities for arbitrary degrees of incompatibility based on ontology/model differences. However, even if nobody were to implement IIIF systems using RDF technologies, I think there are still benefits. Two stand out for me:

### The "Open World Test"

The Open World assumption provides a powerful and useful test of data models and APIs: _"If this data is combined with other data conforming to the same model/API, or with LD conforming to LD best practices, will it make sense or lead to contradictions or confusions?"._ Key examples include contextual information (e.g. proxy in OAI-ORE) and ordering (actually a context issue too; non-contextualizing approaches fail the test).

### Thinking extensible

Related to Open World thinking, a good pattern or way of thinking is that models and APIs should be designed to allow or ignore additional information or extensions wherever possible. This supports extension, allows loser coupling of community work, and help to future proof work by tempering tendencies to be overly prescriptive based on current community The flip side of this is that notions of validation and conformance require more thought. Namespaces are very useful here.

### Inverse: If IIIF uses linked data, should I use a linked data stack to implement it?

The short answer is "no", most IIIF implementations are not based on RDF technologies. There may be situations where it makes sense to implement a complete IIIF stack based on RDF technologies. I'm sure that certain components are a very good match, for example annotation servers. However, I think one should not fall for the following fallacy:

### The "Mi data es su data" fallacy

It is often thought that linked (open) data means that one's internal data and model is the data and model that everyone else should see and use. In many (most?) cases this is wrong. Examples where this is problematic include: internal data that makes the model more complicated and less useful for consumers, inefficiency of RDF as an internal format, difficulty of logging and change management in RDF data, and separation of private and public data.

---

_| [Index](../README.md) | [Next: Image API](../image-api/README.md) |_