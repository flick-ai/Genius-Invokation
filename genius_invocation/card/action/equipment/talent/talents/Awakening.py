from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Awakening(Character):
    id: int = 214021
    name: str = "Awakening"
    name_ch = "觉醒"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.ELECTRO: 3>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 