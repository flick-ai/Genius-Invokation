from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.GuardianofApepsOasis import *

class AThousandYoung(TalentCard):
    id: int = 227021
    name: str = "A Thousand Young"
    name_ch = "万千子嗣"
    is_action = False
    cost = [{'cost_num': 1, 'cost_type': CostType.DENDRO.value}]
    cost_power = 0
    character = GuardianofApepsOasis
    def __init__(self) -> None:
        super().__init__()
