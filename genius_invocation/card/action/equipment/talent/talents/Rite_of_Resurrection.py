from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Rite_of_Resurrection(Character):
    id: int = 211081
    name: str = "Rite of Resurrection"
    name_ch = "起死回骸"
    is_action = True
    cost = [{'cost_num': 5, 'cost_type': <CostType.CRYO: 0>}]
    cost_power = 3
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 