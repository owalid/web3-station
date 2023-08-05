import socket
from uuid import uuid4
from py_server.Client import Client
from py_server.ChallengesConfig import ChallengesConfig
from py_server.utils_strings import apt42_ascii
from py_server.utils import receive_message, send_message

SIZE_OF_RECEIVE = 5
HOST = '0.0.0.0'
PORT = 5554

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
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(socket.SOMAXCONN)
            self.clients = {}
            SocketServer.__instance = self
            print(f"SocketServer initialized listening on {HOST}:{PORT}")

    def exit_client(self, conn, index_client):
        if conn:
            conn.close()
        self.clients[index_client] = None

    def counts_address_clients(self, address):
        count = 0
        for client in self.clients:
            if self.clients[client].address == address:
                count += 1
        return count
    
    def start_server(self):
        challenges_config = ChallengesConfig.get_instance()
        try:
            while True:
                conn, addr = self.server_socket.accept()
                print("Connected by", addr)
                index = uuid4()
                count_address = self.counts_address_clients(addr[0])

                if count_address > 20:
                    send_message(conn, b"Too many connections\n")
                    conn.close()
                    break

                if self.clients.get(index) == None:
                    self.clients[index] = Client(conn, addr)
                else:
                    send_message(conn, b"Already connected\n")
                    conn.close()
                send_message(conn, apt42_ascii.encode())
                while True:
                    send_message(conn, challenges_config.help_menu.encode(), True)
                    r = receive_message(conn, SIZE_OF_RECEIVE)
                    if not r:
                        break
                    action_index = r.decode().strip()
                    if not action_index.isnumeric() or int(action_index) >= len(challenges_config.ACTIONS) or int(action_index) < 0:
                        send_message(conn, action_index.encode() + b" index is not allowed\n")
                        continue
                    else:
                        action = challenges_config.ACTIONS[int(action_index)]
                        action = action.lower()
                        challenge_index = None
                        if action == 'exit':
                            self.exit_client(conn, index)
                            break
                        if action == 'deploy':
                            send_message(conn, challenges_config.challenge_menu.encode())
                            send_message(conn, "[".encode() + str(len(challenges_config.CHALLENGES)).encode() + "]".encode() + b" Return to main menu\n", True)
                            r = receive_message(conn, SIZE_OF_RECEIVE)
                            if not r:
                                break
                            challenge_index = r.decode().strip()
                            if not challenge_index.isnumeric() or int(challenge_index) > len(challenges_config.CHALLENGES) or int(challenge_index) < 0:
                                send_message(conn, challenge_index.encode() + b" index is not allowed\n")
                                continue
                            if int(challenge_index) == len(challenges_config.CHALLENGES):
                                continue
                        self.clients[index].process_action(action.lower(), challenge_index)
        except Exception as e:
            print(e)
            self.exit_client(conn, index)