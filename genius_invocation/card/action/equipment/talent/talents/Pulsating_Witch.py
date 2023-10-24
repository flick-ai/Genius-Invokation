from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Pulsating_Witch(Character):
    id: int = 214091
    name: str = "Pulsating Witch"
    name_ch = "脉冲的魔女"
    is_action = False
    cost = [{'cost_num': 1, 'cost_type': <CostType.ELECTRO: 3>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 