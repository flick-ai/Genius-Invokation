from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Tartaglia import Tartaglia

class AbyssalMayhemHydrospout(TalentCard):
    id: int = 212041
    name: str = "Abyssal Mayhem: Hydrospout"
    name_ch = "深渊之灾·凝水盛放"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 0
    character = Tartaglia
    skill_idx: int = 1
    def __init__(self) -> None:
        super().__init__()
        