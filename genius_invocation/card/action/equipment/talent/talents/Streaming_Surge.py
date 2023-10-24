from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Streaming_Surge(Character):
    id: int = 222011
    name: str = "Streaming Surge"
    name_ch = "百川奔流"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.HYDRO: 1>}]
    cost_power = 3
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 