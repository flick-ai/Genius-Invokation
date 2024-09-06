from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.EremiteFloralRingDancer import *

class KeenEdgedFloralRingBlade(TalentCard):
    id: int = 227031
    name: str = "Keen-Edged Floral Ring-Blade"
    name_ch = "叶轮锋刃"
    time = 5.1
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': CostType.DENDRO.value}]
    cost_power = 0
    character = EremiteFloralRingDancer
    def __init__(self) -> None:
        super().__init__()
