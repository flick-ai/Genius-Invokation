from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Beidou import *

class LightningStorm(TalentCard):
    id: int = 214051
    name: str = "Lightning Storm"
    name_ch = "霹雳连霄"
    time = 3.4
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = Beidou
    def __init__(self) -> None:
        super().__init__()
