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
    if answer == "0x25":
        return True
    return False
