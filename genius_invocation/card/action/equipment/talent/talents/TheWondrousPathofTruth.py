from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Faruzan import *

class TheWondrousPathofTruth(TalentCard):
    id: int = 215091
    name: str = "The Wondrous Path of Truth"
    name_ch = "妙道合真"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 4}]
    cost_power = 2
    character = Faruzan
    def __init__(self) -> None:
        super().__init__()
