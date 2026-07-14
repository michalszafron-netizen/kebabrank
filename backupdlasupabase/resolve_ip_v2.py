import socket
hosts = ['shimhhadhsntguwubeiv.supabase.co', 'db.shimhhadhsntguwubeiv.supabase.co']
for h in hosts:
    try:
        ip = socket.gethostbyname(h)
        print(f"{h}: {ip}")
    except Exception as e:
        print(f"{h}: Error: {e}")
