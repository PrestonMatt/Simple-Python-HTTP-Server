#import sys
from os.path import exists
import requests as rqst
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import ssl
import time
import json
#import socket

class RequestHandler(BaseHTTPRequestHandler):

    locks = {
        "":False,
        "/":False,
        "JUNK":False
    }

    def update_locks(self):
        with open("locks.json","w") as locksfd:
            locksfd.write(json.dumps(self.locks))

    def do_HEAD(self):
        print("Recieved a POST HTTP request.")
        content_len = self.headers.get('Content-Length')
        try:
            request_body = self.rfile.read(int(content_len))
            print(request_body.decode("utf8"))
        except Exception as err:
            return
        
        message = "Test"
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(message))
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        print("Recieved a POST HTTP request.")
        content_len = self.headers.get('Content-Length')
        try:
            request_body = self.rfile.read(int(content_len))
            print(request_body.decode("utf8"))
        except Exception as err:
            return
        
        """
        Process POST Request
        """

        """
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(message))
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        """

        message = "<p>Trying to put your fileback."

        # If the resource is in use, allow a person to check it back in
        try:
            req = request_body.decode("utf8")
            req = req.split("Trying to push file")[1] # cut off the first part
            req = req.split(",")[0] # cut out the content
            req = req[5:]
            req = req[:-1]
            filename = req
        except IndexError:
            message += "\nThere is some error with your filename. Please try again"
            message += "<\p>"
            self.protocol_version = "HTTP/1.1"
            self.send_response(400)
            self.send_header("Content-Length", len(message))
            self.end_headers()
            self.wfile.write(bytes(message, "utf8"))
            return
        
        #print(filename)
        # Get the content:
        try:
            req = request_body.decode("utf8")
            req = req.split("Content\": \"")[1] # cut off the first part
            req = req[:-2] # cut off the "} at the end
            content = req
        except IndexError:
            message += "\nThere is some error with your filename. Please try again"
            message += "<\p>"
            self.protocol_version = "HTTP/1.1"
            self.send_response(400)
            self.send_header("Content-Length", len(message))
            self.end_headers()
            self.wfile.write(bytes(message, "utf8"))
            return
        
        #print(content)

        # Check if the file exists
        extant_bool = exists(filename)
        if(extant_bool):
            message += "\nFile exists"
            
            try:
                if(self.locks[filename] != True):
                    pass
            except:
                self.locks[filename] = False
                message += "\nLooks like the file exists, but hasn't been accessed yet."
                message += "<\p>"
                self.protocol_version = "HTTP/1.1"
                self.send_response(409)
                self.send_header("Content-Length", len(message))
                self.end_headers()
                self.wfile.write(bytes(message, "utf8"))
                # first time accessing the file
                return

            if(self.locks[filename] == True):
                # Step 3: If there is a lock, remove one on the file
                self.locks[filename] = False
                # Step 4: Allow user to edit file.
                message += "\nAll good! Editting checked back in."
                with open(filename,"w") as filed:
                    con = content.replace("\\n","\n")
                    con = con.replace("\\t","\t")
                    # write what was given to the file
                    #filed.write(bytes(content,'utf8'))
                    filed.write(con)
                message += "<\p>"
                self.protocol_version = "HTTP/1.1"
                self.send_response(200)
                self.send_header("Content-Length", len(message))
                self.end_headers()
                self.wfile.write(bytes(message, "utf8"))
            else:
                message += "\nLooks like the file isn't in use. Try again later"
                message += "<\p>"
                self.protocol_version = "HTTP/1.1"
                self.send_response(412)
                self.send_header("Content-Length", len(message))
                self.end_headers()
                self.wfile.write(bytes(message, "utf8"))
        else:
            message += "\nLooks like the file does not exist. I cannot put something back that does not exist."
            message += "<\p>"
            self.protocol_version = "HTTP/1.1"
            self.send_response(404)
            self.send_header("Content-Length", len(message))
            self.end_headers()
            self.wfile.write(bytes(message, "utf8"))

        self.update_locks()

        return

    def do_GET(self):
        print("Recieved a GET HTTP request.")

        content_len = self.headers.get('Content-Length')
        try:
            request_body = self.rfile.read(int(content_len))
            print(request_body.decode("utf8"))
        except Exception as err:
            return
        
        message = "<p>Attempting to retrieve that file for you!"

        """
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(message))
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        """

        """
        Process GET Request
        """
        # Step 1: See if the file exists, if not, create it
        filename = ""
        try:
            req = request_body.decode("utf8").split("Trying to request file")[1]
            req = req[5:]
            req = req[:-2]
            filename = req
        except IndexError:
            message += "\nThere is some error with your filename. Please try again"
            message += "<\p>"
            self.protocol_version = "HTTP/1.1"
            self.send_response(400)
            self.send_header("Content-Length", len(message))
            self.end_headers()
            self.wfile.write(bytes(message, "utf8"))
            return

        extant_bool = exists(filename)
        if(extant_bool):
            message += "\nFile exists"
            # Step 2: See if there is a lock on the file (someone else using it)
            
            try:
                if(self.locks[filename] != True):
                    pass
            except:
                # first time accessing the file
                self.locks[filename] = False

            if(self.locks[filename] != True):
                # Step 3: If no lock, place one on the file
                self.locks[filename] = True
                # Step 4: Allow user to edit file.
                message += "\nAll good! Start editting."
                contents = ""
                with open(filename,"rb") as filed:
                    lines = filed.readlines()
                    for line in lines:
                        contents += str(line)
                message += "<\p>"
                self.protocol_version = "HTTP/1.1"
                self.send_response(200)
                self.send_header("Content-Length", len(message))
                self.send_header("File-Content",contents)
                self.end_headers()
                self.wfile.write(bytes(message, "utf8"))
            else:
                message += "\nLooks like the file is in use. Try again later"
                message += "<\p>"
                self.protocol_version = "HTTP/1.1"
                self.send_response(226)
                self.send_header("Content-Length", len(message))
                self.end_headers()
                self.wfile.write(bytes(message, "utf8"))
        else:
            message += "\nLooks like the file does not exist. I cannot loan out something to you that does not exist."
            message += "<\p>"
            self.protocol_version = "HTTP/1.1"
            self.send_response(404)
            self.send_header("Content-Length", len(message))
            self.end_headers()
            self.wfile.write(bytes(message, "utf8"))

        self.update_locks()

        return

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    requests = 20
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
    #passwd = retrieve_password()
    # Open up the server
    # https://docs.python.org/3/library/http.server.html
    
    http_serv = HTTPServer(server, RequestHandler)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        certfile=_certfile,
        keyfile=_keyfile,
        password="YOU PASSWORD HERE!"
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
        print("\n\nWaiting for a new HTTP request.")
        #time.sleep(3)
        http_serv.handle_request()
    
    print("All out of requests!")

def retrieve_password():
    # ~THIS IS TERRIBLE SECURITY, DON'T EVER DO THIS~
    with open("/home/user/Desktop/Simple-Python-HTTP-Server/local_keys/openssl_passphrase.txt","r") as passfd:
        print("Retreiving password...")
        password = passfd.readlines()[0].strip("\n")
    #print("Test...the password is: %s" % password)
    return password

def main():
    run()
    print("Quitting!")

if __name__ == "__main__":
    main()