"""Simple server with Access-Control-Allow-Origin header.

Adapted from
http://stackoverflow.com/questions/21956683/python-enable-access-control-on-simple-http-server
"""

try:  # Python 3
    from http.server import HTTPServer, SimpleHTTPRequestHandler, test as test_orig
    import sys

    def test(*args):
        """Wrap test to look like py2 version."""
        test_orig(*args, port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000)


except ImportError:  # Python 2
    from BaseHTTPServer import HTTPServer, test
    from SimpleHTTPServer import SimpleHTTPRequestHandler


class CORSRequestHandler(SimpleHTTPRequestHandler):
    """Extend SimpleHTTPRequestHandler to add CORS header."""

    def end_headers(self):
        """Add Access-Control-Allow-Origin header to all responses."""
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)


if __name__ == '__main__':
    test(CORSRequestHandler, HTTPServer)
