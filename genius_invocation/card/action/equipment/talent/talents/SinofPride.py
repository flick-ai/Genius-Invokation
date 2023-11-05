from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.KujouSara import *

class SinofPride(TalentCard):
    id: int = 214061
    name: str = "Sin of Pride"
    name_ch = "我界"
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = KujouSara
    def __init__(self) -> None:
        super().__init__()
