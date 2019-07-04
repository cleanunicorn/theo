from http.server import BaseHTTPRequestHandler, HTTPServer


def MakeHTTPRequestHandler(context):
    class HTTPRequestHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super(HTTPRequestHandler, self).__init__(*args, **kwargs)

        def do_GET(self):
            # https://docs.python.org/3.7/library/http.server.html?highlight=basehttprequesthandler#http.server.BaseHTTPRequestHandler
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()

            print("Context", context)

            self.wfile.write(bytes(self.path, "UTF-8"))

    return HTTPRequestHandler


class Server:
    host = None
    port = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        handler = MakeHTTPRequestHandler(context={"server": "postgres"})

        httpd = HTTPServer((self.host, self.port), handler)

        try:
            httpd = httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.socket.close()
            pass
