from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.SangonomiyaKokomi import * 

class TamakushiCasket(TalentCard):
    id: int = 212051
    name: str = "Tamakushi Casket"
    name_ch = "匣中玉栉"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 2
    character = SangonomiyaKokomi
    def __init__(self) -> None:
        super().__init__()
        