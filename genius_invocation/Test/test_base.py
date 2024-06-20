from genius_invocation.game.game import GeniusGame
from genius_invocation.utils import *
from rich import print
import abc

deck1 = {'character': ['Rhodeia_of_Loch'],'action_card': []}
deck2 = {'character': ['Neuvillette',],'action_card': []}

class Character_Message:
    def __init__(self) -> None:
        self.name: str = None
        self.health: int = None
        self.max_health: int = None
        self.weapon: str = None
        self.artifact: str = None
        self.talent: bool = None
        self.status: List = None

class Player_Message:
    def __init__(self, ) -> None:
        self.characters: List[Character_Message]
        self.dice
        self.card
        self.hand
        self.support
        self.summon
        self.team
        
class Game_Message:
    def __init__(self) -> None:
        self.players: List[Player_Message]
        self.round: int
        self.active: int
        self.first: int
        self.phase: GamePhase
        
message = Game_Message()
game = GeniusGame.read_game(message)
print(game.encode_message())
exit()