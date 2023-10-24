from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Sin_of_Pride(Character):
    id: int = 214061
    name: str = "Sin of Pride"
    name_ch = "我界"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.ELECTRO: 3>}]
    cost_power = 2
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 