from typing import TYPE_CHECKING
from genius_invocation.utils import *
from genius_invocation.event.Elemental_Reaction import *

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Heal:
    def __init__(
            self, 
            heal: int, 
            target_character: 'Character'
            ) -> None:
        self.heal_to_character = target_character
        self.heal_to_player = target_character.from_player
        self.heal_num = heal

        


