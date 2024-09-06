from genius_invocation.utils import *
from genius_invocation.card.action.equipment.specialskill.base import SpecialSkillCard
from genius_invocation.entity.status import SpecialSkill
from genius_invocation.event.damage import Damage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class XenochromaticEntity(SpecialSkill):
    name: str = "Xenochromatic Hunter's Ray"
    name_ch = "异色猎刀鳐"
    id = "313001s1"
    cost = [{'cost_num': 2, 'cost_type': CostType.BLACK}]
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None,  card = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        damage = Damage(damage_type=SkillType.OTHER,
                        main_damage_element=ElementType.PHYSICAL,
                        main_damage=2,
                        piercing_damage=0,
                        damage_from=self,
                        damage_to=get_opponent_active_character(game),
                        )
        game.add_damage(damage)
        game.resolve_damage()
        self.check_usage(game)
        game.manager.invoke(EventType.AFTER_USE_SPECIAL, game)


class Xenochromatic(SpecialSkillCard):
    id: int = 313001
    name: str = "Xenochromatic Hunter's Ray"
    name_ch = "异色猎刀鳐"
    time: float = 5.0
    cost_num: int = 0
    cost_type: CostType = None

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = XenochromaticEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
