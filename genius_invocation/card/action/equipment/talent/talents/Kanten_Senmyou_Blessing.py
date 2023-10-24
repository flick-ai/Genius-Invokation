from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Kanten_Senmyou_Blessing(Character):
    id: int = 211051
    name: str = "Kanten Senmyou Blessing"
    name_ch = "寒天宣命祝词"
    is_action = False
    cost = [{'cost_num': 2, 'cost_type': <CostType.CRYO: 0>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 