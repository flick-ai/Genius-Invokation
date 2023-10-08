from card.players import CHARACTER_STATES
from game.player import GeniusPlayer
from game.action import Action
from utils import *

class GameState:
    def __init__(self):
        self.cur_player: int
        self.first_player: bool
        self.active_player: bool
        player0 = GeniusPlayer(player0_deck)
        player1 = GeniusPlayer(player1_deck)
        self.players = [player0, player1]

        self.game_phase: GamePhase

    def resolve_action(self, action: Action):
        pass    
