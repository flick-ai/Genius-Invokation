#id = 211101
from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Charlotte import *

class aSummationofInterest(TalentCard):
    id: int = 211101
    name: str = "A Summation of Interest"
    name_ch = "以有趣相关为要义"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 0}]
    cost_power = 0
    character = Charlotte
    def __init__(self) -> None:
        super().__init__()
