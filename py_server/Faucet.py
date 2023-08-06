from web3 import Web3
from dotenv import load_dotenv
from os import getenv
from py_server.utils import *

load_dotenv()

MAX_ETHER = 5*10**18
WEB3_PRIVATE_KEY=getenv("WEB3_PRIVATE_KEY")
WEB3_PUBLIC_KEY=getenv("WEB3_PUBLIC_KEY")
WEB3_RPC_URL=getenv("WEB3_RPC_URL")

class Faucet:
    __instance = None

    @staticmethod
    def get_instance():
        '''
        Static access method. used to make singleton.
        '''
        if Faucet.__instance == None:
            Faucet()
        return Faucet.__instance

    def __init__(self):
        if Faucet.__instance != None:
            return Faucet.__instance
        else:
            self.web3 = Web3(Web3.HTTPProvider(WEB3_RPC_URL))
            Faucet.__instance = self

    def send_ether(self, to_address, logger: logging.Logger):
        try:
            if len(to_address) != 42 or Web3.is_address(to_address) == False:
                logger.warning("invalid address submitted: %s", to_address)
                return -1
        except:
            logger.warning("could not parse address: %s", to_address)
            return -1

        current_balance = self.web3.eth.get_balance(to_address)
        if current_balance >= MAX_ETHER:
            logger.warning("balance of address %s already exceed configured amount %d > %d", to_address, current_balance, MAX_ETHER)
            return -2
        try:
            to_send = MAX_ETHER - current_balance
            nonce = self.web3.eth.get_transaction_count(WEB3_PUBLIC_KEY)
            tx = {'nonce': nonce, 'to': to_address, 'value': to_send, 'gas': 3000000, 'gasPrice': self.web3.eth.gas_price }
            signed_tx = self.web3.eth.account.sign_transaction(tx, WEB3_PRIVATE_KEY)
            self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            logger.info("successfully sent %d wei to %s", to_send, to_address)
            return 0
        except:
            return -1
