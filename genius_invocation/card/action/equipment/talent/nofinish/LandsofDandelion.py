from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Qin import * 

class LandsofDandelion(TalentCard):
    id: int = 215021
    name: str = "Lands of Dandelion"
    name_ch = "蒲公英的国土"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 4}]
    cost_power = 3
    character = Qin
    def __init__(self) -> None:
        super().__init__()
        