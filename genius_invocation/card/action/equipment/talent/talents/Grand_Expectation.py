from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Grand_Expectation(Character):
    id: int = 213031
    name: str = "Grand Expectation"
    name_ch = "冒险憧憬"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.PYRO: 2>}]
    cost_power = 2
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 