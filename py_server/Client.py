from socket import socket
from py_server.utils import receive_message, send_message, send_error
from py_server.Contract import Contract
from py_server.Faucet import Faucet
from py_server.utils import getClientLogger, destroyLogger

class Client:
    def __init__(self, conn: socket, addr, uuid):
        self.conn = conn
        self.address = addr
        self.uuid = uuid 
        self.current_deploy = None
        self.logger = getClientLogger(self)
        self.logger.info(f"new connection from %s:%d", self.address[0], self.address[1])

    def __del__(self):
        # It's normal if this function doesn't trigger instantly btw.
        self.logger.info(f"client disconnected %s:%d", self.address[0], self.address[1])
        destroyLogger(self)

    def faucet(self, to_address=''):
        if to_address == '':
            send_message(self.conn, b'You need to provide an address\n\n')
            return
        try:
            res = Faucet.get_instance().send_ether(to_address, self.logger)
        except Exception as e:
            self.logger.critical(e)
            send_error(self.conn, 'An error has occured while providing you with ethers.')
            return
        if res == 0:
            send_message(self.conn, b'Some juicy ethers was sent\n\n')
        elif res == -1:
            send_message(self.conn, b'Your address is invalid\n\n')
        elif res == -2:
            send_message(self.conn, b'You already have enough ethers\n\n')

    def list(self, challenge_index):
        send_message(self.conn, b"\n")
        send_message(self.conn, Contract(int(challenge_index), self.conn, self.logger).get_challenge_info().encode())

    def deploy(self, challenge_index=''):
        if self.current_deploy:
            send_message(self.conn, b'You already have a deployed challenge, it will replace the current one. Do you want to continue? [y/n] ', True)
            r = receive_message(self.conn, 5)
            if not r or r.decode().strip().lower() not in ['y', 'n']:
                send_message(self.conn, b'Invalid input\n\n')
                return
            if r.decode().strip().lower() == 'n':
                send_message(self.conn, b'Ok, not replacing it\n\n')
                return

        try:
            self.current_deploy = Contract(int(challenge_index), self.conn, self.logger)
            if self.current_deploy.challenge_config['deployable'] == True:
                self.current_deploy.deploy()
        except Exception as e:
            self.logger.critical(e)
            self.current_deploy = None
            send_error(self.conn, 'An error has occured while deploying the contract.')
            return
        send_message(self.conn, b'\nChallenge deployed !\n\n')
        send_message(self.conn, self.current_deploy.get_challenge_info().encode())

    def validate(self):
        if not self.current_deploy:
            send_message(self.conn, b'\nYou need to deploy a challenge first\n\n')
            return
        send_message(self.conn, b'\nValidating...\n\n')
        try:
            result, msg = self.current_deploy.validate(self.conn)
        except Exception as e:
            self.logger.critical(e)
            self.current_deploy = None
            send_error(self.conn, 'An error has occured while validating the challenge.')
            return
        send_message(self.conn, msg.encode())
        if result == True:
            del self.current_deploy
            self.current_deploy = None

    def help(self):
        send_message(self.conn, b"""
To get started, grabbed some ether using the `[3] Faucet`.
Then, deploy the contract of your choice using the `[2] Deploy`.
Once you think the objective has been validated, use the `[4] Validate`
\n""")
        pass

    def process_action(self, action, params=None):
        if hasattr(self, action) and callable(job_function := getattr(self, action)):
            if params:
                return job_function(params)
            return job_function()
        return self.help()
