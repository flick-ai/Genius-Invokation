from genius_invocation.card.action.equipment.talent.import_head import *


class Crossfire(TalentCard):
    id: int = 213021
    name: str = "Crossfire"
    name_ch = "交叉火力"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 2}]
    cost_power = 0
    character = Xiangling
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        