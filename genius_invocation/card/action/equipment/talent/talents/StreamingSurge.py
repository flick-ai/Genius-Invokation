from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Rhodeia_of_Loch import Rhodeia_of_Loch

class StreamingSurge(TalentCard):
    id: int = 222011
    name: str = "Streaming Surge"
    name_ch = "百川奔流"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 1}]
    cost_power = 3
    character = Rhodeia_of_Loch
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        