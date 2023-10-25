from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Venti import * 

class EmbraceofWinds(TalentCard):
    id: int = 215031
    name: str = "Embrace of Winds"
    name_ch = "绪风之拥"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 4}]
    cost_power = 0
    character = Venti
    def __init__(self) -> None:
        super().__init__()
        