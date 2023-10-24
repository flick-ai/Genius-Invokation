from genius_invocation.card.action.equipment.talent.import_head import *


class DescentofDivinity(TalentCard):
    id: int = 216041
    name: str = "Descent of Divinity"
    name_ch = "神性之陨"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 5}]
    cost_power = 0
    character = Albedo
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        