from genius_invocation.card.action.equipment.talent.import_head import *


class LandsofDandelion(Character):
    id: int = 215021
    name: str = "Lands of Dandelion"
    name_ch = "蒲公英的国土"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 4}]
    cost_power = 3
    character = Qin
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        