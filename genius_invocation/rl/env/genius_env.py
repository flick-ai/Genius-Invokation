import gymnasium as gym
from genius_invocation.game.game import GeniusGame
from genius_invocation.main import code_to_deck

class GeniusInvocationEnv(gym.Env):
    '''
        Environment for Genius Invocation with the standard gym API.
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

    def encode_state(self):
        # encode deck

        # encode support

        # encode dice
        pass



