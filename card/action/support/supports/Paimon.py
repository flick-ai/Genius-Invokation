from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Paimon_Entity(Support):
    id: int = 322001
    name = 'Paimon'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.idx:
            self.from_player.dice_zone.add([DiceType.OMNI.value, DiceType.OMNI.value,])

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]



class Paimon(SupportCard):
    id: int = 322001
    name: str = 'Paimon'
    cost_num = 3
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Paimon_Entity(game, from_player=game.active_player)
        target_idx = game.current_action.target_idx
        game.active_player.support_zone.add_entity(self.entity, target_idx)
