from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Xiao import * 

class ConquerorofEvilGuardianYaksha(TalentCard):
    id: int = 215041
    name: str = "Conqueror of Evil: Guardian Yaksha"
    name_ch = "降魔·护法夜叉"
    time = 3.7
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 4}]
    cost_power = 2
    character = Xiao
    def __init__(self) -> None:
        super().__init__()
        