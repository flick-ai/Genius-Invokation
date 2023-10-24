from genius_invocation.card.action.equipment.talent.import_head import *


class ChaoticEntropy(Character):
    id: int = 215011
    name: str = "Chaotic Entropy"
    name_ch = "混元熵增论"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 4}]
    cost_power = 2
    character = Sucrose
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        