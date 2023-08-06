import yaml
import os
from yaml.loader import SafeLoader
import logging
from sys import stdout

logger = logging.getLogger('utils')

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

def render_current_challenge(contract) -> str:
    tlc = '\u256D'
    trc = '\u256E'
    blc = '\u2570'
    brc = '\u256F'
    h = '\u2500'
    v = '\u2502'
    line1 = f"Current challenge: {contract.challenge_config['name']}"
    line2 = f"Difficulty: {contract.get_printable_difficulty()}"
    line2len = len(f"Difficulty: {contract.get_difficulty_colorless()}")
    line3 = f"Address: {contract.contract_address}"
    maxlen = max([len(line1), line2len, len(line3)])

    return f" {tlc}{h * maxlen}{trc}\n {v}{line1}{' ' * (maxlen - len(line1))}{v}\n {v}{line2}{' ' * (maxlen - line2len)}{v}\n {v}{line3}{' ' * (maxlen - len(line3))}{v}\n {blc}{h * maxlen}{brc}\n\n"


def destroyLogger(client):
    del logging.Logger.manager.loggerDict[f'client:{client.address[0]}:{client.address[1]}:{client.uuid}']

def getClientLogger(client):
    logger = logging.getLogger(f'client:{client.address[0]}:{client.address[1]}:{client.uuid}')
    logger.propagate = False
    ch = logging.StreamHandler(stdout)
    formatter = logging.Formatter(f'{client.address[0]}:{client.address[1]} %(levelname)s %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

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
        logger.warning(e)
        return None
