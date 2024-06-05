from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.ConsecratedFlyingSerpent import *

class DeathlyCyclone(TalentCard):
    id: int = 225031
    name: str = "Deathly Cyclone"
    name_ch = "亡风啸卷"
    is_action = False
    cost = [{'cost_num': 1, 'cost_type': CostType.ANEMO.value}]
    cost_power = 0
    character = ConsecratedFlyingSerpent
    def __init__(self) -> None:
        super().__init__()
