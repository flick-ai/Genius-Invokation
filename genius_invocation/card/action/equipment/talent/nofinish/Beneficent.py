from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Yaoyao import * 

class Beneficent(TalentCard):
    id: int = 217041
    name: str = "Beneficent"
    name_ch = "慈惠仁心"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 6}]
    cost_power = 0
    character = Yaoyao
    def __init__(self) -> None:
        super().__init__()
        