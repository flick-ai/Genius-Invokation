from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.ConsecratedScorpion import *

class FatalFulmination(TalentCard):
    id: int = 224051
    name: str = "Fatal Fulmination"
    name_ch = "亡雷凝蓄"
    is_action = False
    cost = [{'cost_num': 1, 'cost_type': CostType.ELECTRO.value}]
    cost_power = 0
    character = ConsecratedScorpion
    def __init__(self) -> None:
        super().__init__()
