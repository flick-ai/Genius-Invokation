from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Lynette import * 

class A_Cold_Blade_Like_a_Shadow(TalentCard):
    id: int = 215081
    name: str = "Keen Sight"
    name_ch = "如影流露的冷刃"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 4}]
    cost_power = 0
    character = Lynette
    def __init__(self) -> None:
        super().__init__()
        