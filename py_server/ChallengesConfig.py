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
            config = sorted(config, key=lambda x: x['difficulty_level'])
            self.config = config
            self.ACTIONS = ['Help', 'Deploy', 'Faucet', 'Validate', 'Exit']
            self.CHALLENGES = [conf['name'] for conf in self.config]
            self.help_menu = "Actions:\n" + "\n".join([f"[{i}] {a}" for i, a in enumerate(self.ACTIONS)]) + "\n"
            self.challenge_menu = "Challenge available:\n" + "\n".join([f"[{i}] {a}" for i, a in enumerate(self.CHALLENGES)]) + "\n"
            ChallengesConfig.__instance = self

    def get_config(self):
        return self.config