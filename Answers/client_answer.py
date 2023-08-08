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
    # https://docs.python.org/3/library/http.client.html

    url = "127.0.0.1"
    port = 443
    HTTP_Methods = ["GET","POST"]
    for method in HTTP_Methods:
        conn = http.client.HTTPConnection(
            url,
            port
        ) 
        headers = {'Content-type': 'application/json'}
        data = {'JUNK':'Testing...'}
        data_json = json.dumps(data)
        conn.request(
            method,
            "/",
            data_json,
            headers
        )
        response = conn.getresponse()
        print("Status: {} and reason: {}".format(response.status, response.reason))

        conn.close()

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