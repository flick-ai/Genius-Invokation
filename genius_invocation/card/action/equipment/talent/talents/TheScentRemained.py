from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Xingqiu import Xingqiu

class TheScentRemained(TalentCard):
    id: int = 212021
    name: str = "The Scent Remained"
    name_ch = "重帘留香"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 1}]
    cost_power = 0
    character = Xingqiu
    skill_idx: int = 1
    def __init__(self) -> None:
        super().__init__()
        