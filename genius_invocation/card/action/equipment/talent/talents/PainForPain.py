from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.LaSignora import * 

class PainForPain(TalentCard):
    id: int = 221021
    name: str = "Pain For Pain"
    name_ch = "苦痛奉还"
    is_action = False
    cost = [{'cost_num': 3, 'cost_type': 7}]
    cost_power = 0
    character = LaSignora
    def __init__(self) -> None:
        super().__init__()
        