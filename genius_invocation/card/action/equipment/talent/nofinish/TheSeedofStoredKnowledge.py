from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Tighnari import * 

class TheSeedofStoredKnowledge(TalentCard):
    id: int = 217031
    name: str = "The Seed of Stored Knowledge"
    name_ch = "心识蕴藏之种"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 6}]
    cost_power = 2
    character = Tighnari
    def __init__(self) -> None:
        super().__init__()
        