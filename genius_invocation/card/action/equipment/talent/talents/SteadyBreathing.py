from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Chongyun import *

class SteadyBreathing(TalentCard):
    id: int = 211041
    name: str = "Steady Breathing"
    name_ch = "吐纳真定"
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 0}]
    cost_power = 0
    character = Chongyun
    def __init__(self) -> None:
        super().__init__()
