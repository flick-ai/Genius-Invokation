from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Kaveh import *

class TheArtofBudgeting(TalentCard):
    id: int = 217081
    name: str = "The Art of Budgeting"
    name_ch = "预算师的技艺"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': CostType.DENDRO.value}]
    cost_power = 0
    character = Kaveh
    time = 4.7
    def __init__(self) -> None:
        super().__init__()
