from genius_invocation.card.action.equipment.talent.import_head import *


class KantenSenmyouBlessing(TalentCard):
    id: int = 211051
    name: str = "Kanten Senmyou Blessing"
    name_ch = "寒天宣命祝词"
    is_action = False
    cost = [{'cost_num': 2, 'cost_type': 0}]
    cost_power = 0
    character = Ayaka
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        