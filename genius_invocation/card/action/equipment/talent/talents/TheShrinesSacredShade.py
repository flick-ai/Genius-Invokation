from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Yae_Miko import Yae_Miko

class TheShrinesSacredShade(TalentCard):
    id: int = 214081
    name: str = "The Shrine's Sacred Shade"
    name_ch = "神篱之御荫"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 2
    character = Yae_Miko
    skill_idx: int = 2
    def __init__(self) -> None:
        super().__init__()
        