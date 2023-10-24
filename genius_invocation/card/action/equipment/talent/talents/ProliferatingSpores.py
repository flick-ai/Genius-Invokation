from genius_invocation.card.action.equipment.talent.import_head import *


class ProliferatingSpores(Character):
    id: int = 227011
    name: str = "Proliferating Spores"
    name_ch = "孢子增殖"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 6}]
    cost_power = 0
    character = Fungusgrass
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        