from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Neuvillette import * 

class HeirtotheAncientSeasAuthority(TalentCard):
    id: int = 212101
    name: str = "Heir to the Ancient Sea's Authority"
    name_ch = "古海孑遗的权柄"
    time = 4.5
    is_action = True
    cost = [{'cost_num': 1, 'cost_type': 1}, {'cost_num': 2, 'cost_type': 8}]
    cost_power = 0
    character = Neuvillette
    def __init__(self) -> None:
        super().__init__()
        