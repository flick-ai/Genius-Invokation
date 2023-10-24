from genius_invocation.card.action.equipment.talent.import_head import *


class StreamingSurge(Character):
    id: int = 222011
    name: str = "Streaming Surge"
    name_ch = "百川奔流"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 1}]
    cost_power = 3
    character = Chunshui
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        