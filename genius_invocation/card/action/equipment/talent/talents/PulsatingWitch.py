from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Lisa import * 

class PulsatingWitch(TalentCard):
    id: int = 214091
    name: str = "Pulsating Witch"
    name_ch = "脉冲的魔女"
    time = 4.0
    is_action = False
    cost = [{'cost_num': 1, 'cost_type': 3}]
    cost_power = 0
    character = Lisa
    def __init__(self) -> None:
        super().__init__()
        