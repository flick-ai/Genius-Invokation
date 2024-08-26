from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.HydroHilichurlRogue import *

class FeatherweightFoam(TalentCard):
    id: int = 222051
    name: str = "Featherweight Foam"
    name_ch = "轻盈水沫"
    time = 5.0
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': CostType.HYDRO.value}]
    cost_power = 0
    character = HydroHilichurlRogue
    def __init__(self) -> None:
        super().__init__()
