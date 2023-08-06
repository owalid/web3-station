from py_server.utils import load_config
from py_server.utils_strings import DIFFICULTY
import logging

class ChallengesConfig:
    __instance = None

    @staticmethod
    def get_instance():
        '''
        Static access method. used to make singleton.
        '''
        if ChallengesConfig.__instance == None:
            ChallengesConfig()
        return ChallengesConfig.__instance

    def __init__(self, config=None):
        if ChallengesConfig.__instance != None:
            return ChallengesConfig.__instance
        else:
            self.logger = logging.getLogger('challenges_config')
            self.set_config(config)
            ChallengesConfig.__instance = self

    def set_config(self, config):
        config = sorted(config, key=lambda x: x['difficulty_level'])
        self.config = config
        self.ACTIONS = ['Help', 'List', 'Deploy', 'Faucet', 'Validate', 'Exit']
        self.CHALLENGES = [f"{conf['name']: <20}\t{DIFFICULTY[conf['difficulty_level']]: >5}" for conf in self.config if conf["visibility"] == 1]
        self.help_menu = "Actions:\n" + "\n".join([f"[{i}] {a}" for i, a in enumerate(self.ACTIONS)]) + "\n\n"
        self.challenge_menu = "Challenge available:\n\n" + "\n".join([f"[{i}] {a}" for i, a in enumerate(self.CHALLENGES)]) + "\n"

    def get_config(self):
        return self.config

    def reload_config(self):
        final_data = load_config()
        if final_data is None:
            self.logger.warning('Error loading config file')
            return
        self.set_config(final_data)