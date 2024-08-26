from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Xianyun import *

class TheyCallHerCloudRetainer(TalentCard):
    id: int = 215101
    name: str = "They Call Her Cloud Retainer"
    name_ch = "知是留云僊"
    time = 5.0
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': CostType.ANEMO.value}]
    cost_power = 0
    character = Xianyun
    def __init__(self) -> None:
        super().__init__()
