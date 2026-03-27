import re

# Precompile regex (performance optimization)
VERSION_REGEX = re.compile(r"/([\d\.]+)")

# Scalable server mapping
SERVER_MAP = {
    "apache": "Apache",
    "nginx": "Nginx",
    "iis": "Microsoft IIS",
    "litespeed": "LiteSpeed",
    "cloudflare": "Cloudflare",
    "gunicorn": "Gunicorn"
}


def extract_server_header(response):
    if not response or response.startswith("[ERROR]"):
        return None

    for line in response.splitlines():   # more efficient than split("\n")
        if line.lower().startswith("server:"):
            return line.strip()

    return None


def detect_server_type(server_header):
    if not server_header:
        return "Unknown"

    header = server_header.lower()

    for key, value in SERVER_MAP.items():
        if key in header:
            return value

    return "Unknown"


def extract_version(server_header):
    if not server_header:
        return "Unknown"

    match = VERSION_REGEX.search(server_header)
    return match.group(1) if match else "Unknown"


def analyze_banner(response, protocol="HTTP"):
    server_header = extract_server_header(response)

    # Failure handling
    if not server_header:
        return {
            "Server Type": "Unknown",
            "Version": "Unknown",
            "Protocol": protocol,
            "Status": "Invalid or Missing Banner"
        }

    server_type = detect_server_type(server_header)
    version = extract_version(server_header)

    return {
        "Server Type": server_type,
        "Version": version,
        "Protocol": protocol,
        "Status": "Success"
    }
