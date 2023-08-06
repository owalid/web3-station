import yaml
import os
from yaml.loader import SafeLoader

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

def load_config():
    try:
        with open('challenges.yaml') as file:
            data = yaml.load(file, Loader=SafeLoader)
            final_data = []
            for key, value in data.items():
                with open(value['path']) as sub_file:
                    yml_data = yaml.load(sub_file, Loader=SafeLoader)
                    yml_data['path'] = os.path.dirname(value['path'])
                    yml_data['visibility'] = value['visibility']
                    final_data.append(yml_data)
            return final_data
    except Exception as e:
        print(e)
        return None

