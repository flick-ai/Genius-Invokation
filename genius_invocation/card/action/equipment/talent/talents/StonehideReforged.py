from genius_invocation.card.action.equipment.talent.import_head import *


class StonehideReforged(Character):
    id: int = 226011
    name: str = "Stonehide Reforged"
    name_ch = "重铸：岩盔"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 5}]
    cost_power = 2
    character = Rockbrute
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        