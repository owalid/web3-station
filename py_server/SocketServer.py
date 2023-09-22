import socket
from uuid import uuid4
from py_server.Client import Client
from py_server.ChallengesConfig import ChallengesConfig
from py_server.utils_strings import header
from py_server.utils import receive_message, send_message, render_current_challenge
from py_server.Admin import Admin
from os import getenv
from threading import Thread
import logging
from typing import List
from py_server.Client import Client

SIZE_OF_RECEIVE = 128
RECEIVE_TIMOUT = 3600
HOST = '0.0.0.0'
SECRET_KEY = getenv('SECRET_KEY')
PORT = 5555

class SocketServer:
    __instance = None

    @staticmethod
    def get_instance():
        '''
        Static access method. used to make singleton.
        '''
        if SocketServer.__instance == None:
            SocketServer()
        return SocketServer.__instance

    def __init__(self):
        if SocketServer.__instance != None:
            return SocketServer.__instance
        else:
            self.logger = logging.getLogger('tcpserver')
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(socket.SOMAXCONN)
            self.clients: List[Client] = []
            SocketServer.__instance = self
            self.logger.info(f"SocketServer initialized and listening on {HOST}:{PORT}")

    def exit_client(self, conn, client):
        if conn:
            conn.close()
        _, index = self.get_client_by_uuid(client.uuid)
        # remove client from list
        if index is not None and index < len(self.clients):
            self.clients.pop(index)

    def get_client_by_uuid(self, uuid):
        for i in range(len(self.clients)):
            if self.clients[i].uuid == uuid:
                return self.clients[i], i
        return None, None
    

    def counts_address_clients(self, address):
        count = 0
        for i in range(len(self.clients)):
            if self.clients[i].address == address:
                count += 1
        return count
    
    def handle_requests(self, conn, current_client: Client):
        while True:
            if current_client.current_deploy:
                send_message(conn, f"{render_current_challenge(current_client.current_deploy)}\n".encode())
            send_message(conn, self.challenges_config.help_menu.encode(), True)
            r = receive_message(conn, SIZE_OF_RECEIVE)
            if not r:
                break
            action_index = r.decode().strip()

            if action_index == SECRET_KEY:
                Admin(current_client).interactive()
                continue

            if not action_index.isnumeric() or int(action_index) >= len(self.challenges_config.ACTIONS) or int(action_index) < 0:
                send_message(conn, action_index.encode() + b" index is not allowed\n")
                continue
            else:
                action = self.challenges_config.ACTIONS[int(action_index)]
                action = action.lower()
                param_client = None
                if action == 'exit':
                    self.exit_client(conn, current_client)
                    break
                if action == 'list':
                    send_message(conn, b'\n')
                    send_message(conn, self.challenges_config.challenge_menu.encode())
                    send_message(conn, "\n[".encode() + str(len(self.challenges_config.CHALLENGES)).encode() + "]".encode() + b" Return to main menu\n\n", True)
                    r = receive_message(conn, SIZE_OF_RECEIVE)
                    if not r:
                        break
                    param_client = r.decode().strip()
                    if not param_client.isnumeric() or int(param_client) > len(self.challenges_config.CHALLENGES) or int(param_client) < 0:
                        send_message(conn, param_client.encode() + b" index is not allowed\n\n")
                        continue
                    if int(param_client) == len(self.challenges_config.CHALLENGES):
                        continue
                if action == 'deploy':
                    send_message(conn, b'\n')
                    send_message(conn, self.challenges_config.challenge_menu.encode())
                    send_message(conn, "\n[".encode() + str(len(self.challenges_config.CHALLENGES)).encode() + "]".encode() + b" Return to main menu\n\n", True)
                    r = receive_message(conn, SIZE_OF_RECEIVE)
                    if not r:
                        break
                    param_client = r.decode().strip()
                    if not param_client.isnumeric() or int(param_client) > len(self.challenges_config.CHALLENGES) or int(param_client) < 0:
                        send_message(conn, param_client.encode() + b" index is not allowed\n\n")
                        continue
                    if int(param_client) == len(self.challenges_config.CHALLENGES):
                        continue
                if action == 'faucet':
                    send_message(conn, b'Send me your address, I will send you some ethers\n', True)
                    r = receive_message(conn, SIZE_OF_RECEIVE)
                    if not r:
                        break
                    param_client = r.decode().strip()

                current_client.process_action(action.lower(), param_client)

        self.exit_client(conn, current_client)

    def start_server(self):
        self.challenges_config = ChallengesConfig.get_instance()
        try:
            while True:
                conn, addr = self.server_socket.accept()
                uuid = uuid4()
                count_address = self.counts_address_clients(addr[0])

                if count_address > 20:
                    send_message(conn, b"Too many connections\n")
                    conn.close()
                    break

                if not addr:
                    send_message(conn, b"An error occurred, please try again\n")
                    conn.close()
                    break

                already_connected, _ = self.get_client_by_uuid(uuid)
                if already_connected is None:
                    conn.settimeout(RECEIVE_TIMOUT)
                    current_client = Client(conn, addr, uuid4())
                    self.clients.append(current_client)
                else:
                    send_message(conn, b"Already connected\n")
                    conn.close()
                send_message(conn, header.encode())
                # start thread for client
                thread = Thread(target=self.handle_requests, args=(conn, current_client))
                thread.start()

        except Exception as e:
            self.logger.warning(e)
            self.exit_client(conn, current_client)
