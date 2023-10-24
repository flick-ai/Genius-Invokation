from genius_invocation.card.action.equipment.talent.import_head import *


class KeenSight(Character):
    id: int = 217021
    name: str = "Keen Sight"
    name_ch = "眼识殊明"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 6}]
    cost_power = 0
    character = Tighnari
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        