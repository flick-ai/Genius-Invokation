from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Ningguang import Ningguang

class StrategicReserve(TalentCard):
    id: int = 216011
    name: str = "Strategic Reserve"
    name_ch = "储之千日，用之一刻"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 5}]
    cost_power = 0
    character = Ningguang
    skill_idx: int = 1
    def __init__(self) -> None:
        super().__init__()
        