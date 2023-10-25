from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Maidenwater import * 

class MirrorCage(TalentCard):
    id: int = 222021
    name: str = "Mirror Cage"
    name_ch = "镜锢之笼"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 1}]
    cost_power = 0
    character = Maidenwater
    def __init__(self) -> None:
        super().__init__()
        