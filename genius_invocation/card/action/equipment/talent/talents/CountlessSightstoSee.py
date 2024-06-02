from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Kirara import *

class CountlessSightstoSee(TalentCard):
    id: int = 217071
    name: str = "Countless Sights to See"
    name_ch = "沿途百景会心"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 0}]
    cost_power = 0
    character = Kirara
    def __init__(self) -> None:
        super().__init__()
