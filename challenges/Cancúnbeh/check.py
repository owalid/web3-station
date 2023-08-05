from web3 import Web3
from typing import Dict

def check(w3: Web3, abi: Dict, address: str):
    return w3.eth.contract(address=address, abi=abi).functions.locked().call() == False
