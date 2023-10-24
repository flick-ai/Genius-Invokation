from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Prophecy_of_Submersion(Character):
    id: int = 212031
    name: str = "Prophecy of Submersion"
    name_ch = "沉没的预言"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.HYDRO: 1>}]
    cost_power = 3
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 