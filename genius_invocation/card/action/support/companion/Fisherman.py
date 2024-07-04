from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from genius_invocation.card.action.base import ActionCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support
from genius_invocation.entity.status import Combat_Status

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Cleanup_Entity(Combat_Status):
    name: str = 'Called In For Cleanup'
    name_ch = '清洁工作'
    max_usage = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.add_num = 1

    def update(self):
        self.add_num = min(2, self.add_num + 1)

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == get_my_active_character(game):
            game.current_damage.main_damage += self.add_num
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
        ]


class Cleanup(ActionCard):
    name = "Called In For Cleanup"
    name_ch = "清洁工作"
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        entity = game.active_player.team_combat_status.has_status(Cleanup_Entity)
        if entity is None:
            game.active_player.team_combat_status.add_entity(Cleanup_Entity(game, from_player=game.active_player))
        else:
            try:
                entity.update(game)
            except:
                entity.update()

class Fisherman_Entity(Support):
    id: int = 322025
    name: str = 'The White Glove and the Fisherman'
    name_ch = '白手套和渔夫'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2

    def on_end(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.from_player.card_zone.insert_randomly([Cleanup()], 5)
            self.usage -= 1
            if self.usage == 1:
                self.from_player.get_card(num=1)
            if self.usage == 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_end)
        ]

class Fisherman(SupportCard):
    id: int = 322025
    name: str = 'The White Glove and the Fisherman'
    name_ch = '白手套和渔夫'
    time = 4.6
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Fisherman_Entity(game, from_player=game.active_player)
        super().on_played(game)



