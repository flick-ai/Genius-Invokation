from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Paid_in_Full(Character):
    id: int = 223011
    name: str = "Paid in Full"
    name_ch = "悉数讨回"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.PYRO: 2>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = Fatui_Pyro_Agent
        self.skill_idx = 1
