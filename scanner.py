import socket
import sys #used to read cmd args and cahnge files
import time


if len(sys.argv)<2:  # makes sure there is atleast one argument to work on
    print("syntax: python scanner.py args")
    sys.exit()

sites=sys.argv[1:] #converts all the arguments into a list

def collect_banner(host, port=80):
    s = socket.socket()
    s.settimeout(5)

    s.connect((host, port))

    request = "HEAD / HTTP/1.1\r\nHost: " + host + "\r\n\r\n"
    s.send(request.encode())

    response = s.recv(1024)

    s.close()

    return response.decode(errors="ignore")

def parse_banner(response):
    lines = response.split("\n")

    for line in lines:
        if "Server:" in line:
            return line.strip()

    return "Server header not found"

for target in sites: # iteration thru all the arguments  
    time.sleep(1) # congestion control
    try:
        print("Scanning:", target)

        response = collect_banner(target)

        banner = parse_banner(response)

        print("Banner:", banner)

    except Exception as e:
        print("Error:", e)



