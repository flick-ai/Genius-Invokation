from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Abyssal_Mayhem_Hydrospout(Character):
    id: int = 212041
    name: str = "Abyssal Mayhem: Hydrospout"
    name_ch = "深渊之灾·凝水盛放"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.HYDRO: 1>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 