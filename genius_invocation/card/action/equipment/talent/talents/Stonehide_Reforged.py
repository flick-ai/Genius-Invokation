from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Stonehide_Reforged(Character):
    id: int = 226011
    name: str = "Stonehide Reforged"
    name_ch = "重铸：岩盔"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.GEO: 5>}]
    cost_power = 2
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 