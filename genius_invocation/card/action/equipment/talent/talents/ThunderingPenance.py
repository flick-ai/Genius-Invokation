from genius_invocation.card.action.equipment.talent.import_head import *


class ThunderingPenance(Character):
    id: int = 214031
    name: str = "Thundering Penance"
    name_ch = "抵天雷罚"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = Keqing
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        