import gymnasium as gym
from genius_invocation.game.game import GeniusGame
from genius_invocation.main import code_to_deck
from genius_invocation.game.action import Action
from genius_invocation.utils import *


class GeniusInvocationEnv:
    '''
        Environment for Genius Invocation.
    '''

    def __init__( 
        self,
        deck1: str,
        deck2: str,
        seed: int = None
        ):
        super().__init__()
        deck1 = code_to_deck(deck1)
        deck2 = code_to_deck(deck2)
        self.deck = [deck1, deck2]
        self.seed = seed
        self.base_env = GeniusGame(deck1, deck2, seed)

    def reset(self):
        self.base_env = GeniusGame(self.deck[0], self.deck[1], self.seed)
        state = self.encode_state()
        return state

    def encode_state(self):
        # encode deck
        
        # encode support

        # encode dice
        pass
    def step(self, action):
        processed_action = Action(*action)
        self.base_env.step(processed_action)

