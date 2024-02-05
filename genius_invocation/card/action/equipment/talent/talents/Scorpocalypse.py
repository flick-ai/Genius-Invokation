from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.EremiteScorchingLoremaster import * 

class Scorpocalypse(TalentCard):
    id: int = 223031
    name: str = "Scorpocalypsen"
    name_ch = "苦痛奉还"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 2}]
    cost_power = 2
    character = EremiteScorchingLoremaster
    def __init__(self) -> None:
        super().__init__()
        