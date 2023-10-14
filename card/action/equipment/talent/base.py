from utils import *
from ..base import EquipmentCard

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.zone import CharacterZone
    from game.player import GeniusPlayer



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