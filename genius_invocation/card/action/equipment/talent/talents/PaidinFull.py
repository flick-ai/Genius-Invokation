from genius_invocation.card.action.equipment.talent.import_head import *


class PaidinFull(TalentCard):
    id: int = 223011
    name: str = "Paid in Full"
    name_ch = "悉数讨回"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 2}]
    cost_power = 0
    character = FatuiPyroAgent
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        