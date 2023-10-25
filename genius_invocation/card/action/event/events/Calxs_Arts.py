from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Calxs_Arts(ActionCard):
    id: int = 332009
    name: str = "Calx's Arts"
    name_ch = '白垩之术'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        add_power = 0
        for character in get_my_standby_character(game):
            if character.power > 0:
                character.power -= 1
                add_power += 1
            if add_power == 2:
                break
        active_character = get_my_active_character(game)
        active_character.power = min(active_character.max_power, active_character.power+add_power)
        
        
