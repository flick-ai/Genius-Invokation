from genius_invocation.card.action.equipment.talent.import_head import *


class BunnyTriggered(TalentCard):
    id: int = 213041
    name: str = "Bunny Triggered"
    name_ch = "一触即发"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 2}]
    cost_power = 0
    character = Ambor
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        