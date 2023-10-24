from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Tamakushi_Casket(Character):
    id: int = 212051
    name: str = "Tamakushi Casket"
    name_ch = "匣中玉栉"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.HYDRO: 1>}]
    cost_power = 2
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 