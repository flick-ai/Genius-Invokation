from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Wanderer import Wanderer

class GalesofReverie(TalentCard):
    id: int = 215061
    name: str = "Gales of Reverie"
    name_ch = "梦迹一风"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 4}]
    cost_power = 0
    character = Wanderer
    skill_idx: int = 1
    def __init__(self) -> None:
        super().__init__()
        