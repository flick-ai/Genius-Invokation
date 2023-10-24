from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Embrace_of_Winds(Character):
    id: int = 215031
    name: str = "Embrace of Winds"
    name_ch = "绪风之拥"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.ANEMO: 4>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 