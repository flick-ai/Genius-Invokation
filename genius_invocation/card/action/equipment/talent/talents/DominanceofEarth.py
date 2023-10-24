from genius_invocation.card.action.equipment.talent.import_head import *


class DominanceofEarth(Character):
    id: int = 216031
    name: str = "Dominance of Earth"
    name_ch = "炊金馔玉"
    is_action = True
    cost = [{'cost_num': 5, 'cost_type': 5}]
    cost_power = 0
    character = Zhongli
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        