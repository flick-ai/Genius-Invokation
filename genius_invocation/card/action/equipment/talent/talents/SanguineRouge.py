from genius_invocation.card.action.equipment.talent.import_head import *


class SanguineRouge(TalentCard):
    id: int = 213071
    name: str = "Sanguine Rouge"
    name_ch = "血之灶火"
    is_action = True
    cost = [{'cost_num': 2, 'cost_type': 2}]
    cost_power = 0
    character = Hutao
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        