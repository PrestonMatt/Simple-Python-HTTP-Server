import sys
import os
import requests
#import socket
#import ssl
#import threading
#from requests.adapters import HTTPAdapter
#from urllib3.util.retry import Retry
from urllib.parse import urlparse
import ssl
import http.client
import json

def test_connection():
    _keyfile = "/home/user/Desktop/Simple-Python-HTTP-Server/local_keys/myCA.key"
    _certfile = "/home/user/Desktop/Simple-Python-HTTP-Server/local_keys/myCA.pem"
    # https://docs.python.org/3/library/http.client.html

    url = "127.0.0.1"
    port = 443
    HTTP_Methods = ["GET","POST"]
    for method in HTTP_Methods:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_cert_chain(
            certfile=_certfile,
            keyfile=_keyfile,
            password="YOUR_CERT_PASSWORD_HERE!"
        )
        ssl._create_default_https_context = ssl._create_unverified_context

        http_client = http.client.HTTPSConnection(
            url,
            port
        )
        """
        http_client.sock = context.wrap_socket(
            sock=http_client.sock,
            server_side=False,
            do_handshake_on_connect=True,
            suppress_ragged_eofs=False,
            server_hostname=None,
        )
        """

        headers = {'Content-type': 'application/json'}
        data = {'JUNK':'Testing...'}
        data_json = json.dumps(data)
        http_client.request(
            method,
            "/",
            data_json,
            headers
        )
        response = http_client.getresponse()
        print("Status: {} and reason: {}".format(response.status, response.reason))

        http_client.close()

    """
    with requests.Session() as session:
        #retry = Retry(connect=3, backoff_factor=0.5)
        #adapter = HTTPAdapter(max_retries=retry)
        #session.mount('http://', adapter)
        #session.mount('https://', adapter)

        header = "GET /file.txt HTTP/1.1"

        
        print("Starting the test")
        response = session.get(url, verify=False)
        response.close()
        print("Test response:\n\t%s" % response.content)"""

def process(cmd:str) -> bool:
    if(cmd.lower() == "q" or cmd.lower == "quit"):
        return False
    else:
        #body = cmd
        response = requests.get(URL,verify=False)
        print("Server Response:\n%s" % response)
    return True

def loop():
    breakLoop = True
    while(breakLoop):
        cmd = input(">")
        breakLoop = process(cmd)

def main():
    test_connection()
    #loop()
    print("Quitting!")

if __name__ == "__main__":
    main()