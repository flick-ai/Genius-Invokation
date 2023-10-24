from genius_invocation.card.action.equipment.talent.import_head import *



class AllThingsAreoftheEarth(TalentCard):
    id: int = 217051
    name: str = "All Things Are of the Earth"
    name_ch = "在地为化"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 6}]
    cost_power = 2
    character = Baizhuer
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        