from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.FatuiElectroCicinMage import *

class ElectroCicinsGleam(TalentCard):
    id: int = 24041
    name: str = "Electro Cicins Gleam"
    name_ch = "雷萤浮闪"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': CostType.ELECTRO.value}]
    cost_power = 0
    character = FatuiElectroCicinMage
    def __init__(self) -> None:
        super().__init__()

