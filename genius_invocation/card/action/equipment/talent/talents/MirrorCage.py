from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.MirrorMaiden import *

class MirrorCage(TalentCard):
    id: int = 222021
    name: str = "Mirror Cage"
    name_ch = "镜锢之笼"
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 0
    character = MirrorMaiden
    def __init__(self) -> None:
        super().__init__()
