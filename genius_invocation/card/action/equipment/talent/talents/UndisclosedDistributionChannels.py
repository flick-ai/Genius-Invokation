from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.FrostOperative import *

class UndisclosedDistributionChannels(TalentCard):
    id: int = 216081
    name: str = "Undisclosed Distribution Channels"
    name_ch = "不明流通渠道"
    time = 4.8
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': CostType.CRYO.value}]
    cost_power = 0
    character = FrostOperative
    def __init__(self) -> None:
        super().__init__()
