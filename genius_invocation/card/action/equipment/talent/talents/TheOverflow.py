from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Candace import *

class TheOverflow(TalentCard):
    id: int = 212071
    name: str = "The Overflow"
    name_ch = "衍溢的汐潮"
    time = 3.8
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 2
    character = Candace
    def __init__(self) -> None:
        super().__init__()
