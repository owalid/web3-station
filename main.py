from web3 import Web3
from py_server.ChallengesConfig import ChallengesConfig
from py_server.SocketServer import SocketServer
from py_server.utils import load_config, render_unicode_box
from os import getenv
from dotenv import load_dotenv
import logging
from sys import stdout
import colored_traceback.auto

load_dotenv()

WEB3_PRIVATE_KEY=getenv("WEB3_PRIVATE_KEY")
WEB3_PUBLIC_KEY=getenv("WEB3_PUBLIC_KEY")
WEB3_RPC_URL=getenv("WEB3_RPC_URL")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=stdout)
    final_data = load_config()
    ChallengesConfig(final_data)
    s = SocketServer()
    s.start_server()
