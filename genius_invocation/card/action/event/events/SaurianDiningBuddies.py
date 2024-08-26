from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class SaurianDiningBuddies(ActionCard):
    id: int = 332039
    name: str = 'Saurian Dining Buddies'
    name_ch = "龙伙伴的聚餐"
    time = 5.0
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        character = game.active_player.character_list[game.current_action.target_idx]
        character.character_zone.special_skill.update(usage=1)

    def find_target(self, game: 'GeniusGame'):
        target = []
        for idx, character in enumerate(game.active_player.character_list):
            if character.is_alive and not character.is_frozen:
                if character.character_zone.special_skill != None:
                    target.append(idx+2)
        return target

