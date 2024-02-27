from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write(b"Success! This is a simple HTTP server")
        self.print_request_info()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")

        self._set_response()
        self.wfile.write(b"Success! This is a simple HTTP server")

        self.print_request_info(post_data)

    def print_request_info(self, post_data=None):
        print(f"\nReceived {self.command} request:")
        print(f"Path: {self.path}")
        print(f"Headers: {self.headers}")
        if post_data:
            print(f"Post Data: {post_data}")


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8800):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
