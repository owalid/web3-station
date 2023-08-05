from web3 import Web3
from dotenv import load_dotenv
from os import getenv
load_dotenv()

MAX_ETHER = 5**18
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

    def send_ether(self, to_address):
        if self.web3.eth.get_code(to_address) != b'0x' or len(to_address) != 42 or \
            Web3.is_address(to_address) == False or Web3.is_checksum_address(to_address) == False:
            print("Invalid address!!!!!")
            return -1
        
        current_balance = self.web3.eth.get_balance(to_address)
        if current_balance >= MAX_ETHER:
            return -2

        to_send = MAX_ETHER - current_balance
        nonce = self.web3.eth.get_transaction_count(WEB3_PUBLIC_KEY)
        tx = {'nonce': nonce, 'to': to_address, 'value': to_send, 'gasPrice': self.web3.eth.gas_price }
        signed_tx = self.web3.eth.account.sign_transaction(tx, WEB3_PRIVATE_KEY)
        self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return 0