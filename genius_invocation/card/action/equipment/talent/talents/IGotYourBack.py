from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Noelle import *

class IGotYourBack(TalentCard):
    id: int = 216021
    name: str = "I Got Your Back"
    name_ch = "支援就交给我吧"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 5}]
    cost_power = 0
    character = Noelle
    def __init__(self) -> None:
        super().__init__()
