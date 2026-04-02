import socket
try:
    ip = socket.gethostbyname('kebabrank.com')
    print(f"IP: {ip}")
except Exception as e:
    print(f"Error: {e}")
