from genius_invocation.card.action.equipment.talent.import_head import *


class IGotYourBack(Character):
    id: int = 216021
    name: str = "I Got Your Back"
    name_ch = "支援就交给我吧"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 5}]
    cost_power = 0
    character = Noel
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        