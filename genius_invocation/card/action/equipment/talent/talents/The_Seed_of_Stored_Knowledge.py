from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class The_Seed_of_Stored_Knowledge(Character):
    id: int = 217031
    name: str = "The Seed of Stored Knowledge"
    name_ch = "心识蕴藏之种"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.DENDRO: 6>}]
    cost_power = 2
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 