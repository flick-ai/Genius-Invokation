from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Shaken,_Not_Purred(Character):
    id: int = 211021
    name: str = "Shaken, Not Purred"
    name_ch = "猫爪冰摇"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.CRYO: 0>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 