from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Eula import * 

class WellspringofWarLust(TalentCard):
    id: int = 211061
    name: str = "Wellspring of War-Lust"
    name_ch = "战欲涌现"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 0}]
    cost_power = 2
    character = Eula
    def __init__(self) -> None:
        super().__init__()
        