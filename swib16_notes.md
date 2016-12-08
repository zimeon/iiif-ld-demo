# Notes from SWIB16 workshop, 2016-11-28

See [SWIB16 Programme](http://swib.org/swib16/programme.html)

## Presentation issues

  * Network connectivity was terrible so presenting directly from the web, and having participants download from the web was problematic.
  * Presenting the github rendering of Markdown files like <https://github.com/zimeon/iiif-ld-demo/blob/master/README.md> wasn't great because of the fixed width presentation -- it wasn't possible to scale the text to be easily readable without having the lines go off-screen. Should render that pages to cleaner HTML on gh-pages or similar.
  
## Installation issues

  1. It would really be helpful to have instructions for running under `virtualenv`. This is very simple and fortunately there was a participant ready to help out.
  2. Installation was difficult on Linux systems (seems mostly people had Ubuntu) mainly because of the [CFFI](http://cffi.readthedocs.io/en/latest/) (C Foreign Function Interface) library. In some cases manually running `pip install cffi` was enough, in others it was necessary to uninstall/reinstall/install a system package `python-cffi`. It seems that having the tests on Travis-CI wasn't enough to know that Linux installs would work.
  3. There is no need to be able to run the full set of tests to run the code. The problem is that the test framework uses many more libraries than the example programs themselves need (e.g. `mikasa`) and that is an unnecessary installation burden.
  4. It would help to have installation instructions circulated ahead of time in the hope that participants could do this before for the workshop (on their local networks with good connectivity).

## Participant comments on JSON-LD libraries in languages other than Python

  * JavaScript via npm - works well, very good code, reference implementation
  * Java - Jena support pretty good
  * Ruby - good, also written by Gregg Kellogg

## Comments on IIIF

  * Would be good to make sure that as much of IIIF API is done as hypermedia rather than URI construction/patterns. Example quoted was that in order to make UV handle page numbers correctly these have to be integers.

  