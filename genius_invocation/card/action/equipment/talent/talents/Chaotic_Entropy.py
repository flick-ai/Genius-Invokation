from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Chaotic_Entropy(Character):
    id: int = 215011
    name: str = "Chaotic Entropy"
    name_ch = "混元熵增论"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.ANEMO: 4>}]
    cost_power = 2
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 