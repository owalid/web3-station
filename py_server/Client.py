from py_server.utils import receive_message, send_message
from py_server.Contract import Contract
from py_server.Faucet import Faucet

class Client:
    def __init__(self, conn, address):
        self.address = address
        self.conn = conn
        self.current_deploy = None
    
    def faucet(self, to_address):
        res = Faucet.get_instance().send_ether(to_address)
        if res == 0:
            send_message(self.conn, b'Ether sent')
        elif res == -1:
            send_message(self.conn, b'Your address is invalid')
        elif res == -2:
            send_message(self.conn, b'You already have ether')
        
    
    def deploy(self, challenge_index):
        if self.current_deploy:
            send_message(self.conn, b'You already have a deployed challenge, it will replace the current one. Do you want to continue? [y/n]', True)
            r = receive_message(self.conn, 5)
            if not r or r.decode().strip().lower() not in ['y', 'n']:
                send_message(self.conn, b'Invalid input')
                return
            if r.decode().strip().lower() == 'n':
                send_message(self.conn, b'Ok, not replacing it')
                return
            
        self.current_deploy = Contract(int(challenge_index))
        send_message(self.conn, b'Challenge deployed\n')
        send_message(self.conn, self.current_deploy.get_challenge_info().encode())

    def validate(self):
        if not self.current_deploy:
            send_message(self.conn, b'You need to deploy a challenge first')
            return
        send_message(self.conn, b'Validating...\n')
        result = self.current_deploy.validate()
        send_message(self.conn, result.encode())


    def help(self):
        pass

    def process_action(self, action, params=None):
        if hasattr(self, action) and callable(job_function := getattr(self, action)):
            if params:
                return job_function(params)
            return job_function()
        return self.help()
