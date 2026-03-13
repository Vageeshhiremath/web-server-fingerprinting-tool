import socket
import sys #used to read cmd args and change files
import time
from banner_parser import *
from socket_client import *
from asyncio import *

def input_take():
    if len(sys.argv)<2:  # makes sure there is atleast one argument to work on
        print("syntax: python scanner.py args")
        sys.exit()

    sites=sys.argv[1:] #converts all the arguments into a list
    
    return sites

def valid_target(target):
    try:
        socket.gethostbyname(target)
        return True
    except socket.timeout:
        print("Timeout while scanning", target)

    except socket.gaierror:
        print("DNS resolution failed:", target)

    except ConnectionRefusedError:
        print("Connection refused:", target)


def check_security_headers(response):

    headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options"
    ]

    for h in headers:
        if h.lower() in response.lower():
            print("Security header detected:", h)



def scan(sites):
    for target in sites:
        time.sleep(1)

        try:
            if not valid_target(target):
                print("Invalid target:", target)
                continue
            print("\nScanning:", target)

            # Collect banner using collector module
            response = get_banner(target, 80)
            protocol = "HTTP"

            if not response:
                response = get_banner(target,443)
                protocol = "HTTPS"

            if not response:
                print("no response recieved")
                continue

            check_security_headers(response)
            result = analyze_banner(response, protocol)


            print_result(result)

            print("\n")

        except Exception as e:
            print("Error:", e)