from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.ThunderManifestation import * 

class GrievingEcho(TalentCard):
    id: int = 224021
    name: str = "Grieving Echo"
    name_ch = "悲号回唱"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = ThunderManifestation
    def __init__(self) -> None:
        super().__init__()
        