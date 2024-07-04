from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Layla import *

class LightsRemit(TalentCard):
    id: int=211091
    name: str = "Light's Remit"
    name_ch = "归芒携信"
    time = 4.3
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 0}]
    cost_power = 0
    character = Layla
    def __init__(self) -> None:
        super().__init__()