import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
from pathlib import Path
from socketserver import ThreadingMixIn


class PreviewHandler(SimpleHTTPRequestHandler):
    def log_message(self, format_string, *arguments):
        return


class PreviewServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8081)
    arguments = parser.parse_args()
    os.chdir(str(Path(__file__).resolve().parent))
    server = PreviewServer(('127.0.0.1', arguments.port), PreviewHandler)
    print('Preview: http://127.0.0.1:{}/'.format(arguments.port), flush=True)
    server.serve_forever()