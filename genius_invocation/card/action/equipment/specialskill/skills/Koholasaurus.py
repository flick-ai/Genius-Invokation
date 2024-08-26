from genius_invocation.utils import *
from genius_invocation.card.action.equipment.specialskill.base import SpecialSkillCard
from genius_invocation.entity.status import SpecialSkill
from genius_invocation.event.damage import Damage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class KoholasaurusEntity(SpecialSkill):
    name: str = "Koholasaurus"
    name_ch = "鳍游龙"
    id = "313003s1"
    cost = [{'cost_num': 2, 'cost_type': CostType.WHITE}]
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2

    def on_call(self, game: 'GeniusGame'):
        self.from_player.summon_zone.space[game.current_action.target_idx].on_end_phase(game)

    def find_target(self, game: 'GeniusGame'):
        target = []
        for i in range(self.from_player.summon_zone.num()):
            target.append(i+5)
        return target




class Koholasaurus(SpecialSkillCard):
    id: int = 313003
    name: str = "Koholasaurus"
    name_ch = "鳍游龙"
    time: float = 5.0
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = KoholasaurusEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
