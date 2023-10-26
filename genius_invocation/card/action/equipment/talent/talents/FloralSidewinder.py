from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Collei import * 

class FloralSidewinder(TalentCard):
    id: int = 217011
    name: str = "Floral Sidewinder"
    name_ch = "飞叶迴斜"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 6}]
    cost_power = 0
    character = Collei
    def __init__(self) -> None:
        super().__init__()
        