from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Embers_Rekindled(Character):
    id: int = 223021
    name: str = "Embers Rekindled"
    name_ch = "烬火重燃"
    is_action = False
    cost = [{'cost_num': 2, 'cost_type': <CostType.PYRO: 2>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 