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

    with rqst.Session() as ssl_sesh:
        # Open up the server
        # https://docs.python.org/3/library/http.server.html
        
        http_serv = HTTPServer(server, RequestHandler)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=_certfile,keyfile=_keyfile)

        http_serv.socket = context.wrap_socket(
            sock=http_serv.socket,
            server_side=True,
            do_handshake_on_connect=False,
            suppress_ragged_eofs=False,
            server_hostname=None,
        )
        #http_serv.socket.load_cert_chain(certfile=_certfile,keyfile=_keyfile)
        
        while(requests > 0):
            requests -= 1
            print("Handling a HTTP request.")
            http_serv.handle_request()
            time.sleep(3)
        
        print("All out of requests!")
    
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=_certfile,keyfile=_keyfile)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(server)
        print("\nWaiting for a client...\n")
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()
            print(conn)
            print(addr)
            #ssock.handle_request()
            #conn.send("Test!".encode('utf8'))
    """

    """
    httpd = HTTPServer(server, RequestHandler)
    
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile, certfile, server_side=True, ssl_version=ssl.PROTOCOL_TLSv1)
    
    httpd.socket = ssl.SSLContext.wrap_socket()
    
    
    while(commands > 0):
        httpd.handle_request()
        print("still connecting...")
    """

def main():
    run()
    print("Quitting!")

if __name__ == "__main__":
    main()