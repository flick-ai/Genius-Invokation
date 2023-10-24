from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Arataki_Ichiban(Character):
    id: int = 216051
    name: str = "Arataki Ichiban"
    name_ch = "荒泷第一"
    is_action = True
    cost = [{'cost_num': 1, 'cost_type': <CostType.GEO: 5>}, {'cost_num': 2, 'cost_type': <CostType.BLACK: 8>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 