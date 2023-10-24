from genius_invocation.card.action.equipment.talent.import_head import *


class StalwartandTrue(Character):
    id: int = 213091
    name: str = "Stalwart and True"
    name_ch = "崇诚之真"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 2}]
    cost_power = 0
    character = Dehya
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        