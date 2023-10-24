from genius_invocation.card.action.equipment.talent.import_head import *


class AratakiIchiban(Character):
    id: int = 216051
    name: str = "Arataki Ichiban"
    name_ch = "荒泷第一"
    is_action = True
    cost = [{'cost_num': 1, 'cost_type': 5}, {'cost_num': 2, 'cost_type': 8}]
    cost_power = 0
    character = Itto
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        