from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Kyouka_Fuushi(Character):
    id: int = 212061
    name: str = "Kyouka Fuushi"
    name_ch = "镜华风姿"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.HYDRO: 1>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 