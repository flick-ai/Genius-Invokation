from genius_invocation.card.action.equipment.talent.import_head import *


class StellarPredator(TalentCard):
    id: int = 214011
    name: str = "Stellar Predator"
    name_ch = "噬星魔鸦"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = Fischl
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        