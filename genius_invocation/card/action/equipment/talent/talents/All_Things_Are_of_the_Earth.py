from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class All_Things_Are_of_the_Earth(Character):
    id: int = 217051
    name: str = "All Things Are of the Earth"
    name_ch = "在地为化"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.DENDRO: 6>}]
    cost_power = 2
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 