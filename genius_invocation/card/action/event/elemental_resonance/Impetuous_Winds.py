from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Impetuous_Winds(ActionCard):
    id: int = 331502
    name: str = "Impetuous_Winds"
    name_ch = "迅捷之风"
    cost_num = 1
    card_type = ActionCardType.EVENT_ELEMENTAL_RESONANCE
    cost_type = CostType.ANEMO

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        player = game.active_player
        target_idx = game.current_action.target_idx
        game.manager.invoke(EventType.ON_CHANGE_CHARACTER, game)
        player.change_to_id(target_idx)
        game.is_change_player = False
        player.dice_zone.add([DiceType.OMNI.value])
    
    def find_target(self, game: 'GeniusGame'):
        target_list = []
        for idx, character in enumerate(game.active_player.character_list):
            if character.is_alive and not character.is_active:
                target_list.append(idx+2)
        return target_list