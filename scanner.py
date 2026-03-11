import socket
import sys #used to read cmd args and cahnge files
import time
from banner_parser import *

def input_take():
    if len(sys.argv)<2:  # makes sure there is atleast one argument to work on
        print("syntax: python scanner.py args")
        sys.exit()

    sites=sys.argv[1:] #converts all the arguments into a list
    return sites

def collect_banner(host, port=443): 
    """ function for collecting information from the server
     serevr port 80 is for http
       """
    s = socket.socket()
    s.settimeout(5)

    s.connect((host, port))

    request = "HEAD / HTTP/1.1\r\nHost: " + host + "\r\n\r\n"
    s.send(request.encode())

    response = s.recv(1024)

    s.close()

    return response.decode(errors="ignore")


"""
def parse_banner(response):
    lines = response.split("\n")

    for line in lines:
        if "Server:" in line:
            return line.strip()

    return "Server header not found"
"""

def scan(sites):
    for target in sites: # iteration thru all the arguments  
        time.sleep(1) # congestion control
        try:
            print("\n")
            response=collect_banner(target)
            print("Scanning:", target)
            result = analyze_banner(response,"HTTPS")
            print_result(result)
            print("\n")
        


        except Exception as e:
            print("Error:", e)



