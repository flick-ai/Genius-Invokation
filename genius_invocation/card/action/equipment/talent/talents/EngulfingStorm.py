from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.AbyssLectorVioletLightning import *

class EngulfingStorm(TalentCard):
    id: int = 224061
    name: str = "Surging Undercurrent"
    name_ch = "侵雷重闪"
    time = 5.1
    is_action = False
    cost = [{'cost_num': 1, 'cost_type': CostType.ELECTRO.value}]
    cost_power = 0
    character = AbyssLectorVioletLightning
    def __init__(self) -> None:
        super().__init__()
