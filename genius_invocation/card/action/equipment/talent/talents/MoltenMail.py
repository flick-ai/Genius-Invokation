from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.EmperorofFireandIron import *

class MoltenMail(TalentCard):
    id: int = 223041
    name: str = "Molten Mail"
    name_ch = "熔火铁甲"
    is_action = False
    cost = [{'cost_num': 1, 'cost_type': CostType.PYRO.value}]
    cost_power = 0
    character = EmperorofFireandIron
    def __init__(self) -> None:
        super().__init__()
