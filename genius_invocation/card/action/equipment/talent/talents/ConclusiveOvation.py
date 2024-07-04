#id = 213101
from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Lyney import *

class ConclusiveOvation(TalentCard):
    id: int = 213101
    name: str = "Conclusive Ovation"
    name_ch = "完场喝彩"
    time = 4.3
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 2}]
    cost_power = 0
    character = Lyney
    def __init__(self) -> None:
        super().__init__()
