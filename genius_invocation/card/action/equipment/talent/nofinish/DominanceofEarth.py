from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Zhongli import * 

class DominanceofEarth(TalentCard):
    id: int = 216031
    name: str = "Dominance of Earth"
    name_ch = "炊金馔玉"
    is_action = True
    cost = [{'cost_num': 5, 'cost_type': 5}]
    cost_power = 0
    character = Zhongli
    def __init__(self) -> None:
        super().__init__()
        