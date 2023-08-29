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
    if (contract.functions.balanceOf(answer).call() == 57896044618658097711785492504343953926634992332820282019728792003956564819969):
        return True
    return False
