from utils import *
from game.game import GeniusGame
from ..base import EquipmentCard


class TalentCard(EquipmentCard):
    '''
        天赋牌
    '''
    card_type = ActionCardType.EQUIPMENT_TALENT
    is_action: bool
    def __init__(self) -> None:
        super().__init__()
        
    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
        pass