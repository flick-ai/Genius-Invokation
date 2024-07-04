from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Xinyan import *

class RockininaFlamingWorld(TalentCard):
    id: int = 213121
    name: str = "Rockin' in a Flaming World"
    name_ch = "地狱里摇摆"
    time = 4.7
    is_action = True
    cost = [{'cost_num': 1, 'cost_type': CostType.PYRO.value}, {'cost_num': 2, 'cost_type': 8}]
    cost_power = 0
    character = Xinyan
    def __init__(self) -> None:
        super().__init__()
