from genius_invocation.card.action.equipment.talent.import_head import *


class TheOverflow(Character):
    id: int = 212071
    name: str = "The Overflow"
    name_ch = "衍溢的汐潮"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 1}]
    cost_power = 2
    character = Candace
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        