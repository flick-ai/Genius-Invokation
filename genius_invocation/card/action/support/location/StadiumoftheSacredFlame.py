from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support
from genius_invocation.entity.status import Status

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class AddDamageEntity(Status):
    id: int = 32102231
    name = "Add Damage"
    name_ch = "增加伤害"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2

    def on_add_damage(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            game.current_damage.damage += 1

    def on_final_end(self, game:'GeniusGame'):
        self.usage -= 1
        if self.usage == 0:
            self.on_destroy(game)


    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE_ZONE, self.on_add_damage),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE_ZONE, self.on_final_end),
        ]


class StadiumoftheSacredFlameEntity(Support):
    name = 'Central Laboratory Ruins'
    name_ch = '圣火竞技场'
    max_usage = 6
    id = 32102261
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.contendingfire = 0

    def excute(self, game):
        active_character = get_active_character(game, self.from_player.index)
        if self.contendingfire == 2:
            dices = self.from_player.roll_dice(num=1, is_basic=True)
            self.from_player.dice_zone.add(dices)
        elif self.contendingfire == 4:
            active_character.heal(2, game)
        elif self.contendingfire == 6:
            self.from_character.character_zone.add_entity(AddDamageEntity(
                game,
                from_player=self.from_player,
                from_character=active_character
            ))
            self.on_destroy(game)

    def after_use_skill(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            self.contendingfire += 1
            self.excute(game)

    def after_use_special_skill(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            self.contendingfire += 1
            self.excute(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.SUPPORT_ZONE, self.after_use_skill),
            (EventType.AFTER_USE_SPECIAL, ZoneType.SUPPORT_ZONE, self.after_use_special_skill),
        ]

    def show(self):
        return str(self.contendingfire)

class StadiumoftheSacredFlame(SupportCard):
    id: int = 321022
    name = 'Central Laboratory Ruins'
    name_ch = '圣火竞技场'
    time = 5.0
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = StadiumoftheSacredFlameEntity(game, from_player=game.active_player)
        super().on_played(game)