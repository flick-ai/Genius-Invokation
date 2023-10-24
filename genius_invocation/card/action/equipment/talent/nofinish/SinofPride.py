from genius_invocation.card.action.equipment.talent.import_head import *


class SinofPride(TalentCard):
    id: int = 214061
    name: str = "Sin of Pride"
    name_ch = "我界"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 3}]
    cost_power = 2
    character = Sara
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        