import re

def extract_server_header(response):
    if not response:
        return "Server header not found"

    for line in response.split("\n"):
        if line.lower().startswith("server:"):
            return line.strip()

    return "Server header not found"

def detect_server_type(server_header):
    header = server_header.lower()

    if "apache" in header:
        return "Apache"

    elif "nginx" in header:
        return "Nginx"

    elif "iis" in header:
        return "Microsoft IIS"

    elif "litespeed" in header:
        return "LiteSpeed"

    elif "cloudflare" in header:
        return "Cloudflare"

    elif "gunicorn" in header:
        return "Gunicorn"

    else:
        return "Unknown"


def extract_version(server_header):

    match = re.search(r"/([\d\.]+)", server_header)

    if match:
        return match.group(1)

    return "Unknown"


def analyze_banner(response, protocol="HTTP"):

    server_header = extract_server_header(response)

    server_type = detect_server_type(server_header)

    version = extract_version(server_header)

    result = {
        "Server Type": server_type,
        "Version": version,
        "Protocol": protocol
    }

    return result


def print_result(result):

    print("Server Type :", result["Server Type"])
    print("Version     :", result["Version"])
    print("Protocol    :", result["Protocol"])


# Testing analyzer independently
if __name__ == "__main__":

    sample_response = """
HTTP/1.1 200 OK
Date: Tue, 10 Mar 2026
Server: nginx/1.18.0
Content-Type: text/html
"""
    result = analyze_banner(sample_response)

    print("\nFingerprint Result")
    print("------------------")

    print_result(result)
