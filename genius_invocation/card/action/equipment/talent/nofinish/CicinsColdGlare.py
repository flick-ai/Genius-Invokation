from genius_invocation.card.action.equipment.talent.import_head import *


class CicinsColdGlare(TalentCard):
    id: int = 221011
    name: str = "Cicin's Cold Glare"
    name_ch = "冰萤寒光"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 0}]
    cost_power = 0
    character = MageIce
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        