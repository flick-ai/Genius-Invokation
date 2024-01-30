from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Yelan import *

class TurnControl(TalentCard):
    id: int = 212091
    name: str = "Turn Control"
    name_ch = "猜先有方"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 0
    character = Yelan
    def __init__(self) -> None:
        super().__init__()
