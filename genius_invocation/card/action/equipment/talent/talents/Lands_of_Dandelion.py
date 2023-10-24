from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Lands_of_Dandelion(Character):
    id: int = 215021
    name: str = "Lands of Dandelion"
    name_ch = "蒲公英的国土"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': <CostType.ANEMO: 4>}]
    cost_power = 3
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 