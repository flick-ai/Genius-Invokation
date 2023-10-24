from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Undivided_Heart(Character):
    id: int = 211011
    name: str = "Undivided Heart"
    name_ch = "唯此一心"
    is_action = True
    cost = [{'cost_num': 5, 'cost_type': CostType.CRYO}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 