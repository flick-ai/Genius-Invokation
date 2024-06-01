from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Chongyun import *

class RushingHoundSwiftastheWind(TalentCard):
    id: int = 216061
    name: str = "Rushing Hound, Swift as the Wind"
    name_ch = "犬奔·疾如风"
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 0}]
    cost_power = 0
    character = Chongyun
    def __init__(self) -> None:
        super().__init__()
