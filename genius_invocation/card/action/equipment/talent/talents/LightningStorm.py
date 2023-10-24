from genius_invocation.card.action.equipment.talent.import_head import *


class LightningStorm(Character):
    id: int = 214051
    name: str = "Lightning Storm"
    name_ch = "霹雳连霄"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = Beidou
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        