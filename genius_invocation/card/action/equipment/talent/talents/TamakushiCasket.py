from genius_invocation.card.action.equipment.talent.import_head import *


class TamakushiCasket(Character):
    id: int = 212051
    name: str = "Tamakushi Casket"
    name_ch = "匣中玉栉"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 2
    character = Kokomi
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        