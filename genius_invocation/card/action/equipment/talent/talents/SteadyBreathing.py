from genius_invocation.card.action.equipment.talent.import_head import *


class SteadyBreathing(Character):
    id: int = 211041
    name: str = "Steady Breathing"
    name_ch = "吐纳真定"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 0}]
    cost_power = 0
    character = Chongyun
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        