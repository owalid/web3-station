from web3 import Web3
import os
from py_server.ChallengesConfig import ChallengesConfig
from py_server.SocketServer import SocketServer
import yaml
from yaml.loader import SafeLoader
from os import getenv
from dotenv import load_dotenv

load_dotenv()

WEB3_PRIVATE_KEY=getenv("WEB3_PRIVATE_KEY")
WEB3_PUBLIC_KEY=getenv("WEB3_PUBLIC_KEY")
WEB3_RPC_URL=getenv("WEB3_RPC_URL")

if __name__ == "__main__":
    with open('challenges.yaml') as file:
        data = yaml.load(file, Loader=SafeLoader)
        final_data = []
        for key, value in data.items():
            with open(value['path']) as sub_file:
                yml_data = yaml.load(sub_file, Loader=SafeLoader)
                yml_data['path'] = os.path.dirname(value['path'])
                final_data.append(yml_data)
        ChallengesConfig(final_data)
    s = SocketServer()
    s.start_server()
