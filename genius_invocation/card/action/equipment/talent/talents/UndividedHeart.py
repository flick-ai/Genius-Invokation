from genius_invocation.card.action.equipment.talent.import_head import *


class UndividedHeart(Character):
    id: int = 211011
    name: str = "Undivided Heart"
    name_ch = "唯此一心"
    is_action = True
    cost = [{'cost_num': 5, 'cost_type': 0}]
    cost_power = 0
    character = Ganyu
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        