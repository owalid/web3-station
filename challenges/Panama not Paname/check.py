from web3 import Web3
from typing import Dict

def check(w3: Web3, abi: str, address: str):
    contract = w3.eth.contract(address=address, abi=abi)
    return contract.functions.tookWave().call() and contract.functions.location().call() == 1
