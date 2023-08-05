
def receive_message(conn, buffer_size=1024):
    i = 0
    r = b''
    while True:
        try:
            data = conn.recv(buffer_size)
            r += data
            if len(data.decode()) < buffer_size or data == b'':
                return None if not r else r
            i += 1
            if i > 3:
                conn.sendall(b"This action is not allowed\n")
                return None
        except:
            return None if not r else r
    return None if not r else r

def send_message(conn, message, end=False):
    conn.sendall(message)
    if end:
        conn.sendall(b'> ')