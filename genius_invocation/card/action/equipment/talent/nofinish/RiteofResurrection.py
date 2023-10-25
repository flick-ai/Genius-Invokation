from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Qiqi import * 

class RiteofResurrection(TalentCard):
    id: int = 211081
    name: str = "Rite of Resurrection"
    name_ch = "起死回骸"
    is_action = True
    cost = [{'cost_num': 5, 'cost_type': 0}]
    cost_power = 3
    character = Qiqi
    def __init__(self) -> None:
        super().__init__()
        