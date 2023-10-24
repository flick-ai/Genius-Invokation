from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Poetics_of_Fuubutsu(Character):
    id: int = 215051
    name: str = "Poetics of Fuubutsu"
    name_ch = "风物之诗咏"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.ANEMO: 4>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 