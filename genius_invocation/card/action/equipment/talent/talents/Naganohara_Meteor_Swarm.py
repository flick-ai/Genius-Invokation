from genius_invocation.utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Naganohara_Meteor_Swarm(Character):
    id: int = 213051
    name: str = "Naganohara Meteor Swarm"
    name_ch = "长野原龙势流星群"
    is_action = True
    cost = [{'cost_num': 2, 'cost_type': <CostType.PYRO: 2>}]
    cost_power = 0
    def __init__(self) -> None:
        super().__init__()
        self.character = 
        self.skill_idx = 