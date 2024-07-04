from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Thoma import *

class aSubordinatesSkills(TalentCard):
    id: int = 213111
    name: str = "A Subordinate's Skills"
    name_ch = "僚佐的才巧"
    time = 4.4
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 2}]
    cost_power = 2
    character = Thoma
    def __init__(self) -> None:
        super().__init__()

