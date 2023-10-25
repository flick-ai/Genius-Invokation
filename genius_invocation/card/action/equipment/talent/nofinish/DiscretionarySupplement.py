from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Dori import * 

class DiscretionarySupplement(TalentCard):
    id: int = 214101
    name: str = "Discretionary Supplement"
    name_ch = "酌盈剂虚"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 2
    character = Dori
    def __init__(self) -> None:
        super().__init__()
        