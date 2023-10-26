from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Jadeplume_Terrorshroom import *

class ProliferatingSpores(TalentCard):
    id: int = 227011
    name: str = "Proliferating Spores"
    name_ch = "孢子增殖"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 6}]
    cost_power = 0
    character = Jadeplume_Terrorshroom
    def __init__(self) -> None:
        super().__init__()
