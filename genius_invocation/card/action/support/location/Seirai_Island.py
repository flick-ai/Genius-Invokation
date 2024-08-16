from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support
from genius_invocation.entity.status import Status
from genius_invocation.event.damage import Damage

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Distant_Storm(Status):
    name = 'Distant Storm'
    name_ch = '悠远雷暴'
    id = 32101921
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1

    def on_end(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            damage = Damage.create_damage(game,
                                          damage_type=SkillType.SUMMON,
                                          main_damage_element=ElementType.PIERCING,
                                          main_damage=2,
                                          piercing_damage=0,
                                          damage_from=None,
                                          damage_to=self.from_character)
            game.add_damage(damage)
            game.resolve_damage()
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end),
        ]

class Seirai_Island_Entity(Support):
    id: int = 32201961
    name = 'Seirai Island'
    name_ch = '清籁岛'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_heal(self, game:'GeniusGame'):
        game.current_heal.heal_to_character.add_status(
            Distant_Storm(game,
                          game.current_heal.heal_to_player,
                          game.current_heal.heal_to_character))

    def on_end(self, game:'GeniusGame'):
        self.usage -= 1
        if self.usage == 0:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.FINAL_END, ZoneType.SUPPORT_ZONE, self.on_end),
            (EventType.AFTER_HEAL, ZoneType.SUPPORT_ZONE, self.on_heal)
        ]
    def show(self):
        return str(self.usage)

class Seirai_Island(SupportCard):
    id: int = 321019
    name: str = 'Seirai Island'
    name_ch = '清籁岛'
    time = 4.6
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Seirai_Island_Entity(game, from_player=game.active_player)
        super().on_played(game)