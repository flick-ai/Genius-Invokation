from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Cold-Blooded_Strike(Character):
    id: int = 211031
    name: str = "Cold-Blooded Strike"
    name_ch = "冷血之剑"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.CRYO: 0>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 