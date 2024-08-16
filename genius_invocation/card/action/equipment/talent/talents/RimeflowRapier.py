from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Navia import *

class RimeflowRapier(TalentCard):
    id: int = 221041
    name: str = "Rimeflow Rapier"
    name_ch = "冰雅刺剑"
    time = 4.8
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': CostType.GEO.value}]
    cost_power = 0
    character = Navia
    def __init__(self) -> None:
        super().__init__()
