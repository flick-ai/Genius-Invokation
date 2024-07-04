from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Yunjin import *

class DecorousHarmony(TalentCard):
    id: int = 216071
    name: str = "Decorous Harmony"
    name_ch = "庄谐并举"
    time = 4.7
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': CostType.GEO.value}]
    cost_power = 2
    character = Yunjin
    def __init__(self) -> None:
        super().__init__()
