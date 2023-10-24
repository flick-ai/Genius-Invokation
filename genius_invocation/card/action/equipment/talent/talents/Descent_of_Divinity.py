from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Descent_of_Divinity(Character):
    id: int = 216041
    name: str = "Descent of Divinity"
    name_ch = "神性之陨"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.GEO: 5>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 