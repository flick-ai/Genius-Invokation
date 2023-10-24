from genius_invocation.card.action.equipment.talent.import_head import *


class ColdBloodedStrike(Character):
    id: int = 211031
    name: str = "Cold-Blooded Strike"
    name_ch = "冷血之剑"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 0}]
    cost_power = 0
    character = Keaya
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        