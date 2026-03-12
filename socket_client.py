"""
collector/socket_client.py

Collector module for the Web Server Fingerprinting Tool.
Responsible for establishing a raw TCP socket connection to a target server,
sending a minimal HTTP request, and returning the raw response banner.
"""

import socket


# Default timeout (in seconds) for the socket connection attempt
DEFAULT_TIMEOUT = 5


def get_banner(host: str, port: int, timeout: int = DEFAULT_TIMEOUT) -> str:
    """
    Connect to the given host:port via TCP, send a minimal HTTP HEAD request,
    and return the raw response banner as a string.

    Args:
        host    (str): Hostname or IP address of the target server.
        port    (int): Port number to connect to (e.g. 80 for HTTP, 443 for HTTPS).
        timeout (int): Socket timeout in seconds. Defaults to DEFAULT_TIMEOUT.

    Returns:
        str: The raw banner/response received from the server,
             or an error message string if the connection failed.
    """

    # Step 1 – Build the minimal HTTP HEAD request.
    # "HEAD" retrieves only headers (no body), which is enough to fingerprint
    # the server. The request is terminated with two CRLF sequences as per HTTP/1.0.
    request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    try:
        # Step 2 – Create a standard IPv4 TCP socket (AF_INET = IPv4, SOCK_STREAM = TCP).
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            # Step 3 – Set the connection timeout so we don't block indefinitely
            # on unreachable hosts.
            sock.settimeout(timeout)

            # Step 4 – Resolve the hostname and open the TCP connection.
            # socket.connect() raises OSError / socket.gaierror on failure.
            sock.connect((host, port))

            # Step 5 – Send the HTTP HEAD request encoded as bytes (UTF-8).
            sock.sendall(request.encode("utf-8"))

            # Step 6 – Receive the response in chunks and accumulate into a buffer.
            # We keep reading until the server closes the connection or we time out.
            banner_bytes = b""
            while True:
                chunk = sock.recv(4096)   # Read up to 4 KB at a time
                if not chunk:             # Empty bytes → server closed the connection
                    break
                banner_bytes += chunk

        # Step 7 – Decode the raw bytes into a readable string.
        # 'errors="replace"' prevents crashes on non-UTF-8 characters in the banner.
        banner = banner_bytes.decode("utf-8", errors="replace")
        return banner

    # ------------------------------------------------------------------ #
    #  Error handling                                                       #
    # ------------------------------------------------------------------ #

    except socket.timeout:
        # The server did not respond within the allotted timeout period.
        return f"[ERROR] Connection to {host}:{port} timed out after {timeout}s."

    except ConnectionRefusedError:
        # The target actively refused the connection (port closed / firewall drop).
        return f"[ERROR] Connection refused by {host}:{port}."

    except socket.gaierror as e:
        # getaddrinfo() failed – the hostname could not be resolved.
        return f"[ERROR] Invalid host or DNS resolution failed for '{host}': {e}"

    except OSError as e:
        # Catch-all for any other OS-level socket errors (e.g. network unreachable).
        return f"[ERROR] Socket error while connecting to {host}:{port}: {e}"


# ------------------------------------------------------------------ #
#  Quick smoke-test (runs only when this file is executed directly)    #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    # Example: fingerprint example.com on port 80
    test_host = "example.com"
    test_port = 80

    print(f"Connecting to {test_host}:{test_port} …\n")
    banner = get_banner(test_host, test_port)
    print("--- Banner Received ---")
    print(banner)
