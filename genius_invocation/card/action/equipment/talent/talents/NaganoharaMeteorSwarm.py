from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Yoimiya import *

class NaganoharaMeteorSwarm(TalentCard):
    id: int = 213051
    name: str = "Naganohara Meteor Swarm"
    name_ch = "长野原龙势流星群"
    is_action = True
    # 4.7平衡性调整：费用2变为1
    cost = [{'cost_num': 1, 'cost_type': 2}]
    cost_power = 0
    character = Yoimiya
    def __init__(self) -> None:
        super().__init__()
