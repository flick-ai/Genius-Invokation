from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.AbyssHeraldWickedTorrents import *

class SurgingUndercurrent(TalentCard):
    id: int = 222031
    name: str = "Surging Undercurrent"
    name_ch = "暗流涌动"
    time = 4.6
    is_action = False
    cost = [{'cost_num': 1, 'cost_type': 1}]
    cost_power = 0
    character = AbyssHeraldWickedTorrents
    def __init__(self) -> None:
        super().__init__()
