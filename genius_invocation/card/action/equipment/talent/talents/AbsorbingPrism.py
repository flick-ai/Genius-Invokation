from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.ElectroHypostasis import ElectroHypostasis

class AbsorbingPrism(TalentCard):
    id: int = 224011
    name: str = "Absorbing Prism"
    name_ch = "汲能棱晶"
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 2, 'cost_type': 3}]
    cost_power = 0
    character = ElectroHypostasis
    def __init__(self) -> None:
        super().__init__()

