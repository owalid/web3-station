from web3 import Web3
import os
from py_server.ChallengesConfig import ChallengesConfig
from py_server.SocketServer import SocketServer
from py_server.utils import load_config
import yaml
from yaml.loader import SafeLoader
from os import getenv
from dotenv import load_dotenv

load_dotenv()

WEB3_PRIVATE_KEY=getenv("WEB3_PRIVATE_KEY")
WEB3_PUBLIC_KEY=getenv("WEB3_PUBLIC_KEY")
WEB3_RPC_URL=getenv("WEB3_RPC_URL")

if __name__ == "__main__":
    final_data = load_config()
    ChallengesConfig(final_data)
    s = SocketServer()
    s.start_server()
