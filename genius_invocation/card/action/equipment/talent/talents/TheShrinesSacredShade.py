from genius_invocation.card.action.equipment.talent.import_head import *


class TheShrinesSacredShade(Character):
    id: int = 214081
    name: str = "The Shrine's Sacred Shade"
    name_ch = "神篱之御荫"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 2
    character = Yae
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        