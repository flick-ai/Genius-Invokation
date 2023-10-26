from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.StonehideLawachurl import * 

class StonehideReforged(TalentCard):
    id: int = 226011
    name: str = "Stonehide Reforged"
    name_ch = "重铸：岩盔"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 5}]
    cost_power = 2
    character = StonehideLawachurl
    def __init__(self) -> None:
        super().__init__()
        