from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Flowing_Flame(Character):
    id: int = 213011
    name: str = "Flowing Flame"
    name_ch = "流火焦灼"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.PYRO: 2>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 