from genius_invocation.utils import *
from genius_invocation.card.action.equipment.base import EquipmentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.zone import CharacterZone
    from genius_invocation.game.player import GeniusPlayer



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