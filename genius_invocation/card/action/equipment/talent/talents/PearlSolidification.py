from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.MillennialPearlSeahorse import * 

class PearlSolidification(TalentCard):
    id: int = 224031
    name: str = "Pearl Solidification"
    name_ch = "明珠固化"
    time = 4.4
    is_action = False
    cost = [{'cost_num': 0, 'cost_type': 0}]
    cost_power = 0
    character = MillennialPearlSeahorse
    def __init__(self) -> None:
        super().__init__()