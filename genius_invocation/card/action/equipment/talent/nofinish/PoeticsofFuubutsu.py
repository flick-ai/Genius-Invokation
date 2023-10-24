from genius_invocation.card.action.equipment.talent.import_head import *


class PoeticsofFuubutsu(TalentCard):
    id: int = 215051
    name: str = "Poetics of Fuubutsu"
    name_ch = "风物之诗咏"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 4}]
    cost_power = 0
    character = Kazuha
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        