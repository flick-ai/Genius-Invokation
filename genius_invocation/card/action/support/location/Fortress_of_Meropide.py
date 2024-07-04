from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support
from genius_invocation.entity.status import Combat_Status

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Strictly_Prohibited(Combat_Status):
    name = 'Strictly Prohibited'
    name_ch = '严格禁令'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1

    def on_play(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_card.card_type in [ActionCardType.EVENT,
                                  ActionCardType.EVENT_ARCANE_LEGEND,
                                  ActionCardType.EVENT_COUNTRY,
                                  ActionCardType.EVENT_ELEMENTAL_RESONANCE,
                                  ActionCardType.EVENT_FOOD]:
                self.usage -= 1
                game.can_play_card = False

    def on_end(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
           self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_PLAY_CARD, ZoneType.ACTIVE_ZONE, self.on_play),
            (EventType.END_PHASE, ZoneType.ACTIVE_ZONE, self.on_end),
        ]
class Fortress_of_Meropide_Entity(Support):
    id: int = 322018
    name = 'Fortress of Meropide'
    name_ch = '梅洛彼得堡'
    max_usage = -1
    max_count = 4
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.prohibition = 0

    def on_damage(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_damage.damage_to == get_my_active_character(game):
                self.prohibition = min(self.max_count, self.prohibition+1)

    def on_heal(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_heal.heal_to_character == get_my_active_character(game):
                self.prohibition = min(self.max_count, self.prohibition+1)

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.prohibition == self.max_count:
                self.prohibition = 0
                get_opponent(game).team_combat_status.add_entity(
                    Strictly_Prohibited(game, get_opponent(game))
                )

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.SUPPORT_ZONE, self.on_damage),
            (EventType.AFTER_HEAL, ZoneType.SUPPORT_ZONE, self.on_heal),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]
    def show(self):
        return str(self.usage)

class Fortress_of_Meropide(SupportCard):
    id: int = 321018
    name: str = 'Fortress of Meropide'
    name_ch = '梅洛彼得堡'
    time = 4.5
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Fortress_of_Meropide_Entity(game, from_player=game.active_player)
        super().on_played(game)