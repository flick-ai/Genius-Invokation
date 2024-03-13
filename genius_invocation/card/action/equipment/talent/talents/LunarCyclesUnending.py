from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Azhdaha import *

class LunarCyclesUnending(TalentCard):
    id: int = 226022
    name: str = "Lunar Cycles Unending"
    name_ch = "晦朔千引"
    is_action = True
    is_equip = False
    cost = [{'cost_num': 2, 'cost_type': 7}]
    cost_power = 0
    character = Azhdaha
    def __init__(self) -> None:
        super().__init__()