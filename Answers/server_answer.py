import sys
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import ssl

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        content_len = self.headers.get('Content-Length')
        try:
            request_body = self.rfile.read(int(content_len))
            print(request_body.decode("utf8"))
        except Exception as err:
            return
        
        """
        Process GET Request
        """
        message = "Test!"
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(message))
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        return

def run():
    server = ('127.0.0.1', 443)
    httpd = HTTPServer(server, RequestHandler)
    # https://windowsreport.com/create-self-signed-certificate/#:~:text=Use%20OpenSSL%20to%20create%20a%20self-signed%20certificate%201,created%20earlier%20for%20the%20public%2Fprivate%20key%20file.%20
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile = "C:\\OpenSSL-Win32\\bin\\cert.key", certfile = "C:\\OpenSSL-Win32\\bin\\cert.pem", server_side=True, ssl_version=ssl.PROTOCOL_TLSv1)
    print("\nWaiting for a client...\n")
    while(len(commands) > 0):
        httpd.handle_request()
        print("still connecting...")

def main():
    run()
    print("Quitting!")

if __name__ == "__main__":
    main()