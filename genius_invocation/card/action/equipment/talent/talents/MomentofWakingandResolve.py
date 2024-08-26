from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Freminet import *

class MomentofWakingandResolve(TalentCard):
    id: int = 211121
    name: str = "Moment of Waking and Resolve"
    name_ch = "梦晓与决意之刻"
    time = 5.0
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': CostType.CRYO.value}]
    cost_power = 0
    character = Freminet
    def __init__(self) -> None:
        super().__init__()
