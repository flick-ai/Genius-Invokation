from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Dominance_of_Earth(Character):
    id: int = 216031
    name: str = "Dominance of Earth"
    name_ch = "炊金馔玉"
    is_action = True
    cost = [{'cost_num': 5, 'cost_type': <CostType.GEO: 5>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 