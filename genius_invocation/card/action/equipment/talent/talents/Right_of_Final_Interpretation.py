from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Right_of_Final_Interpretation(Character):
    id: int = 213081
    name: str = "Right of Final Interpretation"
    name_ch = "最终解释权"
    is_action = True
    cost = [{'cost_num': 1, 'cost_type': <CostType.PYRO: 2>}, {'cost_num': 2, 'cost_type': <CostType.BLACK: 8>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 