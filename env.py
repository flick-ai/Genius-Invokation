from rlcard.envs import Env 
from game.game import GeniusGame
from enum import Enum


class ChoiceAction(Enum):
    ACTION = 0

class GeniusEnv(Env):

    def __init__(self, config):
        self.name = 'genius-invocation'
        self.game = GeniusGame()
        super().__init__(config)
        self.actions = []
        self.state_shape = []

    
