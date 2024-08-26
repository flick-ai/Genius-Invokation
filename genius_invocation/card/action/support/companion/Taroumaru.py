from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.summon import Summon
from genius_invocation.event.damage import Damage
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Taroumaru_Enraged(Summon):
    name: str = 'Taroumaru Enraged'
    name_ch = '愤怒的太郎丸'
    element = ElementType.PHYSICAL
    id = 32202411
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2

    def on_end_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=2,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]


class Taroumarus_Savings(ActionCard):
    name = "Taroumaru's Savings"
    name_ch = "太郎丸的存款"
    cost_num = 0
    id = 32202471
    cost_type = None
    card_type = ActionCardType.EVENT
    id = 32202471
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        game.active_player.dice_zone.add([DiceType.OMNI.value])


class Taroumaru_Entity(Support):
    id: int = 32202461
    name: str = 'Taroumaru'
    name_ch = '太郎丸'
    max_usage = 4
    max_count = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.savings = [Taroumarus_Savings() for _ in range(4)]
        self.from_player.card_zone.insert_evenly(self.savings)
        self.savings_num = 0

    def on_play_card(self, game: 'GeniusGame') -> None:
        if game.active_player_index == self.from_player.index:
            if game.current_card.name == "Taroumaru's Savings":
                self.savings_num += 1
                if self.savings_num == 2:
                    game.active_player.summon_zone.add_entity(Taroumaru_Enraged(game, self.from_player))
                    self.on_destroy(game)


class Taroumaru(SupportCard):
    id: int = 322024
    name: str = 'Taroumaru'
    name_ch = '太郎丸'
    time = 4.6
    cost_num = 2
    cost_type = CostType.BLACK
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Taroumaru_Entity(game, from_player=game.active_player)
        super().on_played(game)