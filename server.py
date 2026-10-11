#!/usr/bin/env python3
"""Logs incoming GET requests to stdout"""

import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class LoggingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        when = datetime.now(timezone.utc).isoformat()
        client_ip = self.client_address[0]
        request_line = self.raw_requestline.decode("iso-8859-1").rstrip("\r\n")

        text = f"[{when}] {client_ip} sent:\n{request_line}\n"
        if hasattr(self.headers, "as_string"):
            text += self.headers.as_string()
        else:
            text += "\n"
        print(text, flush=True)

        reply = b"ok\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(reply)))
        self.end_headers()
        self.wfile.write(reply)

    def log_message(self, format, *args):
        return


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9090)
    return parser.parse_args()


def main():
    args = get_args()
    server = ThreadingHTTPServer((args.host, args.port), LoggingHandler)
    print(f"listening on http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down", flush=True)
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
