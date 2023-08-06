from web3 import Web3
from colorama import *
from py_server.ChallengesConfig import ChallengesConfig
from py_server.utils_strings import DIFFICULTY, DIFFICULTY_COLORLESS
from py_server.utils import *
from dotenv import load_dotenv
from os import getenv
import sys
import logging
import importlib
load_dotenv()

WEB3_PRIVATE_KEY=getenv("WEB3_PRIVATE_KEY")
WEB3_PUBLIC_KEY=getenv("WEB3_PUBLIC_KEY")
WEB3_RPC_URL=getenv("WEB3_RPC_URL")

class Contract:

    def __init__(self, challenge_index: int, logger: logging.Logger):
        self.logger = logger
        self.challenge_config = ChallengesConfig.get_instance().config[challenge_index].copy()
        self.web3 = Web3(Web3.HTTPProvider(WEB3_RPC_URL))
        self.contract_address = None
        self.abi = None
        self.bin = None
        self.contract = None

    def deploy(self):
        for file in self.challenge_config['files']:
            abi_path = f"{self.challenge_config['path']}/{file['abi']}"
            bin_path = f"{self.challenge_config['path']}/{file['bin']}"
            self.abi = open(abi_path, 'r').read()
            self.bin = open(bin_path, 'r').read()
            self.contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bin)
            Chain_id = self.web3.eth.chain_id
            self.logger.debug("arguments", self.challenge_config['arguments'])
            construct_txn = self.contract.constructor(*self.challenge_config['arguments']).build_transaction({
                'from': WEB3_PUBLIC_KEY,
                'gasPrice': self.web3.eth.gas_price,
                'chainId': Chain_id,
                'nonce': self.web3.eth.get_transaction_count(WEB3_PUBLIC_KEY),
            })
            signed = self.web3.eth.account.sign_transaction(construct_txn, private_key=WEB3_PRIVATE_KEY)
            tx_hash = self.web3.eth.send_raw_transaction(signed.rawTransaction)
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            self.contract_address = tx_receipt.contractAddress
            self.logger.debug(tx_receipt)
            self.logger.info("deployed challenge %s at %s", self.challenge_config['name'], self.contract_address)

    def get_difficulty_colorless(self):
        return DIFFICULTY_COLORLESS[self.challenge_config['difficulty_level']]

    def get_printable_difficulty(self):
        return DIFFICULTY[self.challenge_config['difficulty_level']]

    def get_challenge_info(self):
        res = f"{self.challenge_config['description']}\nDifficulty: {self.get_printable_difficulty()}\n\n"
        # if self.contract_address:
        #     res += f"Contract address: {self.contract_address}\n\n"
        return res

    def validate(self) -> (bool, str):
        # current_path = sys.path # backup current path
        # change path to challenge directory
        sys.path.append(self.challenge_config['path'])
        import check as ContractChecker
        importlib.reload(ContractChecker)
        validated = ContractChecker.check(self.web3, self.abi, self.contract_address)
        # sys.path = current_path
        sys.path.remove(self.challenge_config['path'])
        if validated:
            self.logger.info("validation of challenge %s successfull", self.challenge_config['name'])
            return (True, f"{Back.GREEN}{Style.BRIGHT}SUCCESS{Style.RESET_ALL} Challenge {self.challenge_config['name']} completed successfully\n\nThere is your flag: {self.challenge_config['flag']}\n\n")
        self.logger.info("validation of challenge %s unsuccessfull", self.challenge_config['name'])
        return (False, f"{Back.RED}{Style.BRIGHT}FAIL{Style.RESET_ALL} Challenge {self.challenge_config['name']} not solved yet\n\n")