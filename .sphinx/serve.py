"""Local dev server with custom 404 page support.

Usage: python3 .sphinx/serve.py [port] [directory]
Defaults: port=8000, directory=_build
"""

import http.server
import os
import sys


class DocsHandler(http.server.SimpleHTTPRequestHandler):
    """Serve static files, falling back to 404.html for missing paths."""

    def do_GET(self):
        path = self.translate_path(self.path)
        if not os.path.exists(path) or (
            os.path.isdir(path)
            and not os.path.exists(os.path.join(path, "index.html"))
        ):
            self.path = "/404.html"
        return super().do_GET()

    def log_message(self, format, *args):
        sys.stderr.write("[serve] %s\n" % (format % args))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    directory = sys.argv[2] if len(sys.argv) > 2 else "_build"

    os.chdir(directory)

    server = http.server.HTTPServer(("", port), DocsHandler)
    print(f"Serving {directory}/ at http://localhost:{port} (with 404 support)")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
