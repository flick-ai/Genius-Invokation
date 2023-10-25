from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Fischl import * 

class StellarPredator(TalentCard):
    id: int = 214011
    name: str = "Stellar Predator"
    name_ch = "噬星魔鸦"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = Fischl
    def __init__(self) -> None:
        super().__init__()
        