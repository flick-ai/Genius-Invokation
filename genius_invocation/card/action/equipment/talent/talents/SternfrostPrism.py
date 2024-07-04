from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.CryoHypostasis import *

class SternfrostPrism(TalentCard):
    id: int = 221031
    name: str = "Sternfrost Prism"
    name_ch = "严霜棱晶"
    time = 4.4
    is_action = False
    cost = [{'cost_num': 1, 'cost_type': 0}]
    cost_power = 0
    character = CryoHypostasis
    def __init__(self) -> None:
        super().__init__()
