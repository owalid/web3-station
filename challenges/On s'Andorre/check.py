from socket import socket
from web3 import Web3
from typing import Dict
import logging
from py_server.utils import receive_message, send_message

def check(w3: Web3, abi: Dict, address: str, conn: socket, logger: logging.Logger):
    send_message(conn, "Your address: ")
    answer = receive_message(conn, 50)
    send_message(conn, "\n")
    if not answer:
        return False
    answer = answer.decode().strip()

    contract = w3.eth.contract(address=address, abi=abi)
    if (contract.functions.balanceOf('0xB961EEdF3D9a2b119379BE69dee5069f6C96bBE6').call() == 1809251394333065553493296640760748560207343510400633813116524750123642650624):
        return True
    return False
