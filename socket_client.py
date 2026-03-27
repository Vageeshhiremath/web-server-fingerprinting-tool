import socket
import ssl
import asyncio

DEFAULT_TIMEOUT = 5

def get_banner(host: str, port: int, timeout: int = DEFAULT_TIMEOUT) -> str:
    request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if port == 443:
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)
            sock.connect((host, port))
            sock.sendall(request.encode())
            banner = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                banner += chunk
        return banner.decode(errors="replace")
    except Exception as e:
        return f"[ERROR] {host}:{port} -> {e}"


async def get_banner_async(host: str, port: int, timeout: int = DEFAULT_TIMEOUT) -> str:
    request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    try:
        if port == 443:
            context = ssl.create_default_context()
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port, ssl=context, server_hostname=host),
                timeout=timeout
            )
        else:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=timeout
            )
        writer.write(request.encode())
        await writer.drain()
        banner = await asyncio.wait_for(reader.read(), timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return banner.decode(errors="replace")
    except Exception as e:
        return f"[ERROR] {host}:{port} -> {e}"


async def scan_with_limit(targets, limit=10):
    sem = asyncio.Semaphore(limit)
    async def worker(host, port):
        async with sem:
            return await get_banner_async(host, port)
    tasks = [worker(h, p) for h, p in targets]
    return await asyncio.gather(*tasks)