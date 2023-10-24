from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Sara import * 

class SinofPride(TalentCard):
    id: int = 214061
    name: str = "Sin of Pride"
    name_ch = "我界"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 3}]
    cost_power = 2
    character = Sara
    def __init__(self) -> None:
        super().__init__()
        