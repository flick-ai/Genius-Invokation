from genius_invocation.card.action.equipment.talent.import_head import *


class FlowingFlame(TalentCard):
    id: int = 213011
    name: str = "Flowing Flame"
    name_ch = "流火焦灼"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 2}]
    cost_power = 0
    character = Diluc
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        