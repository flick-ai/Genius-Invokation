from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Alhaitham import *

class Structuration(TalentCard):
    id: int = 217061
    name: str = "Structuration"
    name_ch = "正理"
    time = 4.3
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 6}]
    cost_power = 2
    character = Alhaitham
    def __init__(self) -> None:
        super().__init__()

