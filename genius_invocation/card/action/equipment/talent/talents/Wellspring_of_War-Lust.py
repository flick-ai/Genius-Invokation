from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Wellspring_of_War-Lust(Character):
    id: int = 211061
    name: str = "Wellspring of War-Lust"
    name_ch = "战欲涌现"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.CRYO: 0>}]
    cost_power = 2
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 