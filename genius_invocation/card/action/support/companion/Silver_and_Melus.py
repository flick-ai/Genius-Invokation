from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Silver_and_Melus_Entity(Support):
    id: int = 32202361
    name: str = 'Silver and Melus'
    name_ch = '西尔弗和迈勒斯'
    max_usage = 4
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.attentiveness = 0

    def on_excute_damage(self, game: 'GeniusGame'):
        if game.current_damage.damage_to.from_player == self.from_player:
            self.attentiveness = min(self.max_usage, self.from_player.suffer_damage_type)

    def on_end(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.attentiveness >= 3:
                self.from_player.get_card(num=self.attentiveness)
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_excute_damage),
            (EventType.END_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_end)
        ]

    def show(self):
        return str(self.attentiveness)

class Silver_and_Melus(SupportCard):
    id: int = 322023
    name: str = 'Silver and Melus'
    name_ch = '西尔弗和迈勒斯'
    time = 4.4
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Silver_and_Melus_Entity(game, from_player=game.active_player)
        super().on_played(game)