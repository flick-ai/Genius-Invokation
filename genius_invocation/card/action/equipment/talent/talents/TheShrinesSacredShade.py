from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Yae_Miko import *

class TheShrinesSacredShade(TalentCard):
    id: int = 214081
    name: str = "The Shrine's Sacred Shade"
    name_ch = "神篱之御荫"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 2
    character = Yae_Miko
    def __init__(self) -> None:
        super().__init__()
