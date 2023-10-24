from genius_invocation.card.action.equipment.talent.import_head import *


class MysticalAbandon(Character):
    id: int = 211071
    name: str = "Mystical Abandon"
    name_ch = "忘玄"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 0}]
    cost_power = 0
    character = Shenhe
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        