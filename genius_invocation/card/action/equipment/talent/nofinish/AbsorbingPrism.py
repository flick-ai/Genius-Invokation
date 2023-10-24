from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Effigyelectric import * 

class AbsorbingPrism(TalentCard):
    id: int = 224011
    name: str = "Absorbing Prism"
    name_ch = "汲能棱晶"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = Effigyelectric
    def __init__(self) -> None:
        super().__init__()
        