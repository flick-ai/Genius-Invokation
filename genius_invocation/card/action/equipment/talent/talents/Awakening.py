from genius_invocation.card.action.equipment.talent.import_head import *


class Awakening(TalentCard):
    id: int = 214021
    name: str = "Awakening"
    name_ch = "觉醒"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 3}]
    cost_power = 0
    character = Razor
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        