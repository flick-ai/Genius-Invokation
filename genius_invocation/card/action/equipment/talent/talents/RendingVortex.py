from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Dvalin import *

class RendingVortex(TalentCard):
    id: int = 225021
    name: str = "Rending Vortex"
    name_ch = "毁裂风涡"
    is_action = False
    cost = [{'cost_num': 3, 'cost_type': 4}]
    cost_power = 0
    character = Dvalin
    def __init__(self) -> None:
        super().__init__()
