from genius_invocation.card.action.equipment.talent.import_head import *


class ShakenNotPurred(TalentCard):
    id: int = 211021
    name: str = "Shaken, Not Purred"
    name_ch = "猫爪冰摇"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 0}]
    cost_power = 0
    character = Diona
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        