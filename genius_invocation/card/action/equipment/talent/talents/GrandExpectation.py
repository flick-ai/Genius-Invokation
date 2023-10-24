from genius_invocation.card.action.equipment.talent.import_head import *


class GrandExpectation(Character):
    id: int = 213031
    name: str = "Grand Expectation"
    name_ch = "冒险憧憬"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 2}]
    cost_power = 2
    character = Bennett
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        