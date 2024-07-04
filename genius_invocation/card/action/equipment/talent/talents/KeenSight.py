from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Tighnari import * 

class KeenSight(TalentCard):
    id: int = 217021
    name: str = "Keen Sight"
    name_ch = "眼识殊明"
    time = 3.6
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 6}]
    cost_power = 0
    character = Tighnari
    def __init__(self) -> None:
        super().__init__()
        