from web3 import Web3
from typing import Dict
import logging
from os import getenv

def check(w3: Web3, abi: Dict, address: str, conn, logger: logging.Logger):
    contract = w3.eth.contract(address=address, abi=abi)
    return contract.functions.isSolved().call()
