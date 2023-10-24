from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Cicin's_Cold_Glare(Character):
    id: int = 221011
    name: str = "Cicin's Cold Glare"
    name_ch = "冰萤寒光"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.CRYO: 0>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 