from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Barbara import *

class GloriousSeason(TalentCard):
    id: int = 212011
    name: str = "Glorious Season"
    name_ch = "光辉的季节"
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 0
    character = Barbara
    def __init__(self) -> None:
        super().__init__()
