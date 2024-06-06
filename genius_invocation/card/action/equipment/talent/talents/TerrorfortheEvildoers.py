from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Wriothesley import *

class TerrorfortheEvildoers(TalentCard):
    id: int = 211111
    name: str = "Terror for the Evildoers"
    name_ch = "予行恶者以惩惧"
    is_action = True
    cost = [{'cost_num': 1, 'cost_type': CostType.CRYO.value}, {'cost_num': 2, 'cost_type': 8}]
    cost_power = 0
    character = Wriothesley
    def __init__(self) -> None:
        super().__init__()
