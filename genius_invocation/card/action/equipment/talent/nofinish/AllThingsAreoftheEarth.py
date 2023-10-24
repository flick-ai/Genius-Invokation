from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Baizhuer import * 

class AllThingsAreoftheEarth(TalentCard):
    id: int = 217051
    name: str = "All Things Are of the Earth"
    name_ch = "在地为化"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 6}]
    cost_power = 2
    character = Baizhuer
    def __init__(self) -> None:
        super().__init__()
        