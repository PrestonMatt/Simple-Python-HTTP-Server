#import sys
#import os
import requests as rqst
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import ssl
import time
#import socket

class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        print("Handling POST")
        content_len = self.headers.get('Content-Length')
        try:
            request_body = self.rfile.read(int(content_len))
            print(request_body.decode("utf8"))
        except Exception as err:
            return
        
        """
        Process POST Request
        """
        message = "Test!"
        print("Recieved a GET HTTP request.")
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(message))
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        return

    def do_GET(self):
        print("Handling GET")
        content_len = self.headers.get('Content-Length')
        try:
            request_body = self.rfile.read(int(content_len))
            print(request_body.decode("utf8"))
        except Exception as err:
            return
        
        """
        Process GET Request
        """
        message = input("Say something>") #"Test!"
        print("Recieved a GET HTTP request.")
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(message))
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        return

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    requests = 10
    #https://docs.python.org/3/library/ssl.html

    # If you want to use the build in Ubuntu keys, you can change the following lines to be uncommented:
    #keyfile = "/etc/ssl/private/ssl-cert-snakeoil.key"
    #certfile = "/etc/ssl/certs/ssl-cert-snakeoil.pem"
    _keyfile = "/home/user/Desktop/Simple-Python-HTTP-Server/local_keys/myCA.key"
    _certfile = "/home/user/Desktop/Simple-Python-HTTP-Server/local_keys/myCA.pem"
    # If you want to create and sign your own certificates, see here:
    # https://askubuntu.com/questions/49196/how-do-i-create-a-self-signed-ssl-certificate
    # https://windowsreport.com/create-self-signed-certificate/#:~:text=Use%20OpenSSL%20to%20create%20a%20self-signed%20certificate%201,created%20earlier%20for%20the%20public%2Fprivate%20key%20file.%20
    
    server = ("127.0.0.1", 443)

    # Open up the server
    # https://docs.python.org/3/library/http.server.html
    
    http_serv = HTTPServer(server, RequestHandler)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        certfile=_certfile,
        keyfile=_keyfile,
        password="YOUR_CERT_PASSWORD_HERE!"
    )
    ssl._create_default_https_context = ssl._create_unverified_context

    http_serv.socket = context.wrap_socket(
        sock=http_serv.socket,
        server_side=True,
        do_handshake_on_connect=True,
        suppress_ragged_eofs=False,
        server_hostname=None,
    )
    
    while(requests > 0):
        requests -= 1
        print("Handling a HTTP request.")
        #time.sleep(3)
        http_serv.handle_request()
    
    print("All out of requests!")

def main():
    run()
    print("Quitting!")

if __name__ == "__main__":
    main()