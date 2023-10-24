from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Gales_of_Reverie(Character):
    id: int = 215061
    name: str = "Gales of Reverie"
    name_ch = "梦迹一风"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.ANEMO: 4>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 