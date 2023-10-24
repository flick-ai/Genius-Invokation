from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Beneficent(Character):
    id: int = 217041
    name: str = "Beneficent"
    name_ch = "慈惠仁心"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.DENDRO: 6>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 