from genius_invocation.card.action.equipment.talent.import_head import *


class AbsorbingPrism(Character):
    id: int = 224011
    name: str = "Absorbing Prism"
    name_ch = "汲能棱晶"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = Effigyelectric
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        