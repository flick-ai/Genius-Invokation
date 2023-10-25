from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
import random

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class High_Voltage(ActionCard):
    id: int = 331402
    name: str = "High_Voltage"
    name_ch = "强能之雷"
    elment = ElementType.ELECTRO
    cost_num = 1
    card_type = ActionCardType.EVENT_ELEMENTAL_RESONANCE
    cost_type = CostType.ELECTRO

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        target_character = get_active_character(game, game.active_player.index)
        if target_character.power < target_character.max_power:
            target_character.power += 1
        else:
            standby_character = get_my_standby_character(game)
            for ch in standby_character:
                if ch.power < ch.max_power:
                    ch.power += 1
                    break