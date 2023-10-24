from genius_invocation.card.action.equipment.talent.import_head import *


class FeatherfallJudgment(Character):
    id: int = 214041
    name: str = "Featherfall Judgment"
    name_ch = "落羽的裁择"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = Cyno
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        