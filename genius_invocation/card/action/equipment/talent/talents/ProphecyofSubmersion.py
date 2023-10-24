from genius_invocation.card.action.equipment.talent.import_head import *


class ProphecyofSubmersion(TalentCard):
    id: int = 212031
    name: str = "Prophecy of Submersion"
    name_ch = "沉没的预言"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 3
    character = Mona
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        