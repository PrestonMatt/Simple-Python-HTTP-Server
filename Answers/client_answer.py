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
import subprocess

def test_connection(passwd:str):
    # https://docs.python.org/3/library/http.client.html

    url = "127.0.0.1"
    port = 443
    HTTP_Methods = ["GET","POST","HEAD"]
    for method in HTTP_Methods:

        ssl._create_default_https_context = ssl._create_unverified_context

        http_client = http.client.HTTPSConnection(
            url,
            port
        )

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
        print("Method: {}, status: {} and reason: {}".format(method, response.status, response.reason))

        http_client.close()
    
    print("\n\n(Note, both GET and POST requests are JUNK requests and should return 400)")

def retrieve_password():
    # ~THIS IS TERRIBLE SECURITY, DON'T EVER DO THIS~
    with open("/home/user/Desktop/Simple-Python-HTTP-Server/local_keys/openssl_passphrase.txt","r") as passfd:
        print("Retreiving password...")
        password = passfd.readlines()[0].strip("\n")
    #print("Test...the password is: %s" % password)
    return password

def get_cmd(mthd:str,filename:str) -> bool:

    url = "127.0.0.1"
    port = 443
    header = {}
    _data = {}
    if(mthd == "GET"):
        header = {'Connection': 'file checkout'}
        _data = {'Trying to request file:':filename[1:]}
    elif(mthd == "POST"):
        header = {'Connection': 'file check back in'}
        content = b""
        try:
            with open(filename.strip(".txt") + ".temp","rb") as confd:
                lines = confd.readlines()
                for line in lines:
                    content += line
            # delete file
            print("Deleting temporary file for editting.")
            x = subprocess.Popen(
                ["rm",filename.strip(".txt") + ".temp"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            )
            x.kill()
        except FileNotFoundError:
            print("File does not exist! Pushing empty contents to server.")
        _data = {
            'Trying to push file:':filename[1:],
            'Content':content.decode('utf8')
        }
    
    data_json = json.dumps(_data)

    #ssl._create_default_https_context = ssl._create_unverified_context

    http_client = http.client.HTTPSConnection(
        url,
        port,
    )

    http_client.request(
        mthd,
        filename,
        data_json,
        header
    )
    response = http_client.getresponse()
    #print(response)
    print("Method: {}, status: {} and reason: {}".format(mthd, response.status, response.reason))

    #print(response.headers)

    http_client.close()

    if(response.status == 200 and mthd == "GET"):
        # extract the file data
        with open(filename.strip(".txt") + ".temp","w") as confd:
            # Get the file content and copy to temp file:
            resp_headrs = response.headers
            
            resp_headrs = str(resp_headrs).split("File-Content:")[1]
            resp_headrs = resp_headrs[3:-2]
            
            resp_headrs = resp_headrs.replace("\\n","\n")
            resp_headrs = resp_headrs.replace("\\t","\t")
            resp_headrs = resp_headrs.replace("'b'","")
            resp_headrs = resp_headrs.replace("'","")

            confd.write(str(resp_headrs))
            # allow user to write new data
            print("Please write the appending lines you want to add to the file:")
            try:
                while(True):
                    line = input("#")
                    confd.write(line)
            except KeyboardInterrupt:
                print("\nDone writing lines!")
        return True
    elif(response.status == 200 and mthd == "POST"):
        return True
    return False

def process(cmd:str) -> bool:
    if(cmd.lower() == "q" or cmd.lower == "quit"):
        return False
    else:
        filename = "/" + cmd.split(" ")[1]
        print(filename)
        if(cmd.lower().__contains__("get")):
            success = get_cmd("GET",filename)
            print("Your GET request succeeded: %s" % success)
        elif(cmd.lower().__contains__("post")):
            success = get_cmd("POST",filename)
            print("Your POST request succeeded: %s" % success)
    return True

def loop():
    breakLoop = True
    while(breakLoop):
        cmd = input(">")
        breakLoop = process(cmd)

def main():
    try:
        password = retrieve_password()
        test_connection(password)
        loop()
    except ConnectionRefusedError:
        print("No connection found to server!")
    print("Quitting!")

if __name__ == "__main__":
    main()