from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Soothing_Water(ActionCard):
    id: int = 331102
    name: str = "Shattering_Ice"
    cost_num = 1
    card_type = ActionCardType.EVENT_ELEMENTAL_RESONANCE.value
    cost_type = CostType.HYDRO

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        target_character = get_active_character(game, game.active_player.index)
        target_character.heal(heal=2)
        standby_character = get_my_standby_character(game)
        for ch in standby_character:
            ch.heal(heal=1)