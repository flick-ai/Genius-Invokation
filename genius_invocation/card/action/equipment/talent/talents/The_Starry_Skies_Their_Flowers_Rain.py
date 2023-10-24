from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class The_Starry_Skies_Their_Flowers_Rain(Character):
    id: int = 212081
    name: str = "The Starry Skies Their Flowers Rain"
    name_ch = "星天的花雨"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.HYDRO: 1>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 