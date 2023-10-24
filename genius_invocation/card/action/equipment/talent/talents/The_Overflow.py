from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class The_Overflow(Character):
    id: int = 212071
    name: str = "The Overflow"
    name_ch = "衍溢的汐潮"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.HYDRO: 1>}]
    cost_power = 2
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 