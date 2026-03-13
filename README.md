# web-server-fingerprinting-tool

This project identifies web server type and version by analyzing service banners using TCP socket communication in Python.

## Features
- HTTP banner grabbing
- FTP banner detection
- Server identification (Apache, Nginx, IIS, LiteSpeed)
- Multi-server scanning
- SSL support

## Technologies Used
- Python
- TCP Sockets
- SSL

## Example commands to check
- python main.py httpbin.org
  
Output expected:
Scanning: httpbin.org
Server Type : Gunicorn
Version     : 19.9.0
Protocol    : HTTP
