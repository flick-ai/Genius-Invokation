from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Steady_Breathing(Character):
    id: int = 211041
    name: str = "Steady Breathing"
    name_ch = "吐纳真定"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.CRYO: 0>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 