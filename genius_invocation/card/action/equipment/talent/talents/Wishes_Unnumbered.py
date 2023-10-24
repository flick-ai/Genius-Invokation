from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Wishes_Unnumbered(Character):
    id: int = 214071
    name: str = "Wishes Unnumbered"
    name_ch = "万千的愿望"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.ELECTRO: 3>}]
    cost_power = 2
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 