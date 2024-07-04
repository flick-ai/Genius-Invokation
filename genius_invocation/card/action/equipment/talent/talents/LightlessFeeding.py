from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.AllDevouringNarwhal import *

class LightlessFeeding(TalentCard):
    id: int = 222041
    name: str = "Lightless Feeding"
    name_ch = "无光鲸噬"
    time = 4.7
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': CostType.HYDRO.value}]
    cost_power = 0
    character = AllDevouringNarwhal
    def __init__(self) -> None:
        super().__init__()
