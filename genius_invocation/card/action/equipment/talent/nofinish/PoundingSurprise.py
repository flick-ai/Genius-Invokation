from genius_invocation.card.action.equipment.talent.import_head import *


class PoundingSurprise(TalentCard):
    id: int = 213061
    name: str = "Pounding Surprise"
    name_ch = "砰砰礼物"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 2}]
    cost_power = 0
    character = Klee
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        