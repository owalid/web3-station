from web3 import Web3
from py_server.ChallengesConfig import ChallengesConfig
from dotenv import load_dotenv
from os import getenv
import sys
load_dotenv()

WEB3_PRIVATE_KEY=getenv("WEB3_PRIVATE_KEY")
WEB3_PUBLIC_KEY=getenv("WEB3_PUBLIC_KEY")
WEB3_RPC_URL=getenv("WEB3_RPC_URL")
DIFFICULTY = [
    "Very Easy",
    "Easy",
    "Medium",
    "Hard"
]
class Contract:

    def __init__(self, challenge_index):
        self.challenge_config = ChallengesConfig.get_instance().config[challenge_index].copy()
        self.web3 = Web3(Web3.HTTPProvider(WEB3_RPC_URL))
        for file in self.challenge_config['files']:
            abi_path = f"{self.challenge_config['path']}/{file['abi']}"
            bin_path = f"{self.challenge_config['path']}/{file['bin']}"
            self.abi = open(abi_path, 'r').read()
            self.bin = open(bin_path, 'r').read()
            self.contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bin)
            Chain_id = self.web3.eth.chain_id
            construct_txn = self.contract.constructor().build_transaction({
                'from': WEB3_PUBLIC_KEY,
                'gasPrice': self.web3.eth.gas_price, 
                'chainId': Chain_id,
                'nonce': self.web3.eth.get_transaction_count(WEB3_PUBLIC_KEY),
            })
            signed = self.web3.eth.account.sign_transaction(construct_txn, private_key=WEB3_PRIVATE_KEY)
            tx_hash = self.web3.eth.send_raw_transaction(signed.rawTransaction)
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            self.contract_address = tx_receipt.contractAddress
            print(tx_receipt)

    def get_challenge_info(self):
        return f"{self.challenge_config['description']}\nDifficulty: {DIFFICULTY[self.challenge_config['difficulty_level']]}\nContract address: {self.contract_address}\n\n"
    
    def validate(self):
        current_path = sys.path # backup current path
        # change path to challenge directory
        sys.path.append(self.challenge_config['path'])
        from check import check
        validated = check(self.web3, self.abi, self.contract_address)
        sys.path = current_path
        if validated:
            return f"Challenge {self.challenge_config['name']} completed successfully\n There is your flag: {self.challenge_config['flag']}\n\n"
        return f"Challenge {self.challenge_config['name']} solved failed\n\n"