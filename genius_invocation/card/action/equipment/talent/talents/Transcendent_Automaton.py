from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Transcendent_Automaton(Character):
    id: int = 225011
    name: str = "Transcendent Automaton"
    name_ch = "机巧神通"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': <CostType.ANEMO: 4>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 