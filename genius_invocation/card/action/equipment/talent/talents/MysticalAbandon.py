from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Shenhe import Shenhe

class MysticalAbandon(TalentCard):
    id: int = 211071
    name: str = "Mystical Abandon"
    name_ch = "忘玄"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 0}]
    cost_power = 0
    character = Shenhe
    skill_idx: int = 1
    def __init__(self) -> None:
        super().__init__()
        