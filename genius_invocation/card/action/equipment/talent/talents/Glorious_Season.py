from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Glorious_Season(Character):
    id: int = 212011
    name: str = "Glorious Season"
    name_ch = "光辉的季节"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.HYDRO: 1>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 