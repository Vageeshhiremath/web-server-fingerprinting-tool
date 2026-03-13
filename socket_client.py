"""Collector for raw TCP HTTP banner retrieval."""

import socket
import ssl
# Default socket timeout in seconds
DEFAULT_TIMEOUT = 5


def get_banner(host: str, port: int, timeout: int = DEFAULT_TIMEOUT) -> str:
    """Return raw HTTP banner from host:port or an error string."""
    
    # minimal HEAD request to fetch headers only
    request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)          # avoid hanging
            if port == 443:
                context = ssl.create_default_context()
                s = context.wrap_socket(s, server_hostname=host)
            sock.connect((host, port))       # open TCP connection
            sock.sendall(request.encode("utf-8"))

            # read until the server closes the connection
            banner_bytes = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                banner_bytes += chunk

        return banner_bytes.decode("utf-8", errors="replace")

    except socket.timeout:
        return f"[ERROR] Connection to {host}:{port} timed out after {timeout}s."
    except ConnectionRefusedError:
        return f"[ERROR] Connection refused by {host}:{port}."
    except socket.gaierror as e:
        return f"[ERROR] DNS resolution failed for '{host}': {e}"
    except OSError as e:
        return f"[ERROR] Socket error connecting to {host}:{port}: {e}"


if __name__ == "__main__":
    # quick smoke test
    host = "example.com"
    port = 80
    print(f"Connecting to {host}:{port}...\n")
    print(get_banner(host, port))
