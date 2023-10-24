from genius_invocation.card.action.equipment.talent.import_head import *


class EmbraceofWinds(Character):
    id: int = 215031
    name: str = "Embrace of Winds"
    name_ch = "绪风之拥"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 4}]
    cost_power = 0
    character = Venti
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        