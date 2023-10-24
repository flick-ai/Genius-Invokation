from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Mystical_Abandon(Character):
    id: int = 211071
    name: str = "Mystical Abandon"
    name_ch = "忘玄"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.CRYO: 0>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 