from genius_invocation.card.action.equipment.talent.import_head import *


class Beneficent(TalentCard):
    id: int = 217041
    name: str = "Beneficent"
    name_ch = "慈惠仁心"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 6}]
    cost_power = 0
    character = Yaoyao
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        