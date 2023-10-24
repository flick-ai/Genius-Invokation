from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Jadeplume_Terrorshroom import Jadeplume_Terrorshroom

class ProliferatingSpores(TalentCard):
    id: int = 227011
    name: str = "Proliferating Spores"
    name_ch = "孢子增殖"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 6}]
    cost_power = 0
    character = Jadeplume_Terrorshroom
    skill_idx: int = 1
    def __init__(self) -> None:
        super().__init__()
        