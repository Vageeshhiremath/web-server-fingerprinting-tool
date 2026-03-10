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

## Project Structure

web-server-fingerprinting-tool/
│
├── socket_connection.py
├── fingerprint_engine.py
├── scanner.py
└── targets.txt
