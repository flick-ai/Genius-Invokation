from genius_invocation.card.action.equipment.talent.import_head import *


class KyoukaFuushi(TalentCard):
    id: int = 212061
    name: str = "Kyouka Fuushi"
    name_ch = "镜华风姿"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 0
    character = Ayato
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        