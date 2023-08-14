from web3 import Web3
from typing import Dict
import logging
from os import getenv

def check(w3: Web3, abi: Dict, address: str, conn, logger: logging.Logger):
    return all([w3.eth.contract(address=address, abi=abi).functions.ownerOf(x).call() != getenv("WEB3_PUBLIC_KEY") for x in range(0, 3)])
