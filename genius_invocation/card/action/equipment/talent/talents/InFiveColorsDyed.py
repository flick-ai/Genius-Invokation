from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Chiori import *

class InFiveColorsDyed(TalentCard):
    id: int = 216091
    name: str = "In Five Colors Dyed"
    name_ch = "落染五色"
    time = 5.1
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': CostType.GEO.value}]
    cost_power = 0
    character = Chiori
    def __init__(self) -> None:
        super().__init__()
