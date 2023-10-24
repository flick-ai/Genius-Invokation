from genius_invocation.card.action.equipment.talent.import_head import *


class EmbersRekindled(TalentCard):
    id: int = 223021
    name: str = "Embers Rekindled"
    name_ch = "烬火重燃"
    is_action = False
    cost = [{'cost_num': 2, 'cost_type': 2}]
    cost_power = 0
    character = DeaconFire
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()
        