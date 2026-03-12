import socket
import sys #used to read cmd args and cahnge files
import time
from banner_parser import *
from socket_client import *

def input_take():
    if len(sys.argv)<2:  # makes sure there is atleast one argument to work on
        print("syntax: python scanner.py args")
        sys.exit()

    sites=sys.argv[1:] #converts all the arguments into a list
    return sites


def scan(sites):
    for target in sites:
        time.sleep(1)

        try:
            print("\nScanning:", target)

            # Collect banner using collector module
            response = get_banner(target, 80)

            result = analyze_banner(response, "HTTP")


            print_result(result)

            print("\n")

        except Exception as e:
            print("Error:", e)