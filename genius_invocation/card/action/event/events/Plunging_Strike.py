from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Plunging_Strike(ActionCard):
    id: int = 3320017
    name: str = 'Plunging Strike'
    name_ch = '下落斩'
    cost_num = 3
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        target = game.current_action.target_idx
        game.active_player.change_to_id(target)
        get_my_active_character(game).skill(0, game)

    def find_target(self, game:'GeniusGame'):
        target = []
        for idx, character in enumerate(game.active_player.character_list):
            if not character.is_active and character.is_alive and not character.is_frozen:
                target.append(idx)
        return target
