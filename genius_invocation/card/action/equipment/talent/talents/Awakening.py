from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Razor import *

class Awakening(TalentCard):
    id: int = 214021
    name: str = "Awakening"
    name_ch = "觉醒"
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = Razor
    def __init__(self) -> None:
        super().__init__()
