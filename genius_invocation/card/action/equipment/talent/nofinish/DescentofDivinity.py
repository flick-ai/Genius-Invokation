from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Albedo import * 

class DescentofDivinity(TalentCard):
    id: int = 216041
    name: str = "Descent of Divinity"
    name_ch = "神性之陨"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 5}]
    cost_power = 0
    character = Albedo
    def __init__(self) -> None:
        super().__init__()
        