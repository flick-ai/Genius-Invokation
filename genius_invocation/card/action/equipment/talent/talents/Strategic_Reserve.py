from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Strategic_Reserve(Character):
    id: int = 216011
    name: str = "Strategic Reserve"
    name_ch = "储之千日，用之一刻"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.GEO: 5>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 