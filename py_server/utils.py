import yaml
from socket import socket
import os
from yaml.loader import SafeLoader
import logging
from sys import stdout
from colorama import *

logger = logging.getLogger('utils')

def receive_message(conn: socket, buffer_size=1024):
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

def send_error(conn, message, end=False):
    conn.sendall(f"\n{Back.RED}{Style.BRIGHT}Error:{Style.RESET_ALL} {message} Please contact your administrator.\n\n".encode())
    if end:
        conn.sendall(b'> ')

def send_message(conn, message, end=False):
    if type(message) == str:
        message = message.encode()
    conn.sendall(message)
    if end:
        conn.sendall(b'> ')

import re

def len_no_ansi(string):
    return len(re.sub(
        r'[\u001B\u009B][\[\]()#;?]*((([a-zA-Z\d]*(;[-a-zA-Z\d\/#&.:=?%@~_]*)*)?\u0007)|((\d{1,4}(?:;\d{0,4})*)?[\dA-PR-TZcf-ntqry=><~]))', '', string))

def render_unicode_box(message: str, hc = '') -> str:
    '''
    Draw a unicode box around the message

            Parameters:
                    message (str): the message to be put inside the box
                    hc (str): heading char, placed b4 the unicode box

            Returns:
                    The message inside the box as a string
    '''
    s_message = message.split('\n')
    longest_line = max([len_no_ansi(line) for line in s_message])
    tlc = '\u256D'
    trc = '\u256E'
    blc = '\u2570'
    brc = '\u256F'
    h = '\u2500'
    v = '\u2502'
    a = f"{hc}{tlc}{h * longest_line}{trc}\n"
    for line in s_message:
        a += f"{hc}{v}{line}{' ' * (longest_line - len_no_ansi(line))}{v}\n"
    a += f"{hc}{blc}{h * longest_line}{brc}"
    return a

def render_current_challenge(contract) -> str:
    return render_unicode_box(f"Current challenge: {contract.challenge_config['name']}\n"\
                              f"Difficulty: {contract.get_printable_difficulty()}\n"
                              f"Address: {contract.contract_address}", ' ') + '\n'

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
                    if value['visibility'] == 0:
                        continue
                    yml_data['path'] = os.path.dirname(value['path'])
                    yml_data['visibility'] = value['visibility']
                    final_data.append(yml_data)
            return final_data
    except Exception as e:
        logger.warning(e)
        return None
