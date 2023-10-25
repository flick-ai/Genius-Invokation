from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Sucrose import * 

class ChaoticEntropy(TalentCard):
    id: int = 215011
    name: str = "Chaotic Entropy"
    name_ch = "混元熵增论"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 4}]
    cost_power = 2
    character = Sucrose
    def __init__(self) -> None:
        super().__init__()
        