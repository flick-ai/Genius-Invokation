from genius_invocation.card.action.equipment.talent.import_head import *


class GloriousSeason(Character):
    id: int = 212011
    name: str = "Glorious Season"
    name_ch = "光辉的季节"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 1}]
    cost_power = 0
    character = Barbara
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        