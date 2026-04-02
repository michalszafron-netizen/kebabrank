import socket
try:
    ip = socket.gethostbyname('db.shimhhadhsntguwubeiv.supabase.co')
    print(f"IPv4: {ip}")
except Exception as e:
    print(f"Error: {e}")
