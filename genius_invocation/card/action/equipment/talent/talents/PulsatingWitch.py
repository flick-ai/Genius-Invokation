from genius_invocation.card.action.equipment.talent.import_head import *


class PulsatingWitch(Character):
    id: int = 214091
    name: str = "Pulsating Witch"
    name_ch = "脉冲的魔女"
    is_action = False
    cost = [{'cost_num': 1, 'cost_type': 3}]
    cost_power = 0
    character = Lisa
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        