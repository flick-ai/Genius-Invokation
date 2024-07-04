from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Lynette import * 

class aColdBladeLikeaShadow(TalentCard):
    id: int = 215081
    name: str = "A Cold Blade Like a Shadow"
    name_ch = "如影流露的冷刃"
    time = 4.3
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 4}]
    cost_power = 0
    character = Lynette
    def __init__(self) -> None:
        super().__init__()
        