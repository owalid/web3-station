from socket import socket
from web3 import Web3
from typing import Dict
import logging
from py_server.utils import receive_message, send_message

def check(w3: Web3, abi: Dict, address: str, conn: socket, logger: logging.Logger):
    send_message(conn, "Answer: ")
    answer = receive_message(conn, 50)
    if not answer:
        return False
    answer = answer.decode().strip()
    if answer == "0xae42A3dDc82667012B4608942d6ab1534f1a543a0x0f69D850E415869a2dB986654381c525008c1E530x57d3ea422d9A4907Ad6373E03DeAc653633CEa980x40126b2E329e5fC7cAbb8CDB5c9F9FEB8Fe58A16":
        return True
    return False
