from py_server.Client import Client
import logging
from py_server.utils import receive_message, send_message, render_unicode_box
from py_server.ChallengesConfig import ChallengesConfig
import py_server.SocketServer
from colorama import *

SIZE_OF_RECEIVE = 128

class Admin:
    def __init__(self, client: Client) -> None:
        self.conn = client.conn
        self.logger = client.logger
        self.ACTIONS = {'Reload challenges list': self.reload, 'Notifications': self.notifications}
        self.help = "Admin actions:\n" + "\n".join([f"[{i}] {a}" for i, a in enumerate(self.ACTIONS)]) + "\n\n"
        self.logger.critical("New access to the admin interface")

    def interactive(self):
        while True:
            send_message(self.conn, b'\n')
            send_message(self.conn, self.help.encode())
            send_message(self.conn, "[".encode() + str(len(self.ACTIONS.keys())).encode() + "]".encode() + b" Return to main menu\n\n", True)
            action = receive_message(self.conn, SIZE_OF_RECEIVE)
            if not action:
                break
            action = action.decode().strip()
            if not action.isnumeric() or int(action) > len(self.ACTIONS.keys()) or int(action) < 0:
                send_message(self.conn, action.encode() + b" index is not allowed\n\n")
                continue
            if int(action) == len(self.ACTIONS):
                return

            list(self.ACTIONS.values())[int(action)]()

    def reload(self):
        ChallengesConfig.get_instance().reload_config()
        send_message(self.conn, "\nChallenges have been reloaded\n")
        self.logger.info("Challenges have been reloaded")
        return

    def notifications(self):
        send_message(self.conn, "notification > ")
        o_content = receive_message(self.conn, 1024)
        if not o_content:
            return
        o_content = o_content.decode().strip()
        content = f"\n{Back.RED}{Style.BRIGHT}Notification:{Style.RESET_ALL}\n{render_unicode_box(render_unicode_box(f'{Back.RED}{Style.BRIGHT}{o_content}{Style.RESET_ALL}'))}\n> "

        send_message(self.conn, "send notification ? [y/n] > ")
        confirmation = receive_message(self.conn, SIZE_OF_RECEIVE)
        if not confirmation:
            return
        if confirmation.decode().strip().lower() != 'y':
            return

        self.logger.info("Broadcasting a new notification: %s", o_content)
        server = py_server.SocketServer.SocketServer.get_instance()
        for client in server.clients:
            # Sometimes client will not be remove from the global list of clients because they
            # havent disconnected themself successfully thus we wrap this function around a try/catch
            try:
                send_message(client.conn, content)
            except Exception as e:
                pass