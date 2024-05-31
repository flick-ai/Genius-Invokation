from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.KukiShinobu import * 

class ToWardWeakness(TalentCard):
    id: int = 214111
    name: str = "割舍软弱之心"
    name_ch = "梦迹一风"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 2
    character = KukiShinobu
    def __init__(self) -> None:
        super().__init__()
        