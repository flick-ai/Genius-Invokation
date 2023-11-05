from genius_invocation.utils import *
from genius_invocation.entity.entity import Entity
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.action import Action
    from genius_invocation.event.events import ListenerNode
    from genius_invocation.game.player import GeniusPlayer
    from genius_invocation.entity.character import Character

class Summon(Entity):
    # 召唤物基本类
    id: int
    name: str
    element: ElementType
    removable: bool # 是否能拔掉，若是盾、光降之剑，则在结束回合时按自己的方式爆炸。

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage: int = 0
        self.current_usage: int = self.usage

    def on_destroy(self, game:'GeniusGame'):
        super().on_destroy(game)
        game.manager.invoke(EventType.ON_SUMMON_REMOVE, game)
        self.from_player.summon_zone.remove(self)

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def add_usage(self, game: 'GeniusGame', count: int):
        self.current_usage += count

    def minus_usage(self, game: 'GeniusGame', count: int):
        self.current_usage -= count
        self.current_usage = max(0, self.current_usage)
        if self.current_usage <= 0 and self.removable:
            self.on_destroy(game)

    def show(self):
        return self.current_usage

class Burning_Flame(Summon):
    '''
        燃烧烈焰
    '''

    name = 'Burning Flame'
    name_ch = "燃烧烈焰"
    removable = True
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.element = ElementType.PYRO
        self.current_usage = 1
        self.usage = 1
        self.max_usage = 2

    def update(self):
        self.current_usage += 1
        self.current_usage = min(self.current_usage, self.max_usage)

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            from genius_invocation.event.damage import Damage
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
        if(self.current_usage <= 0):
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]