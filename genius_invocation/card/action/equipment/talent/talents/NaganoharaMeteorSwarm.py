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

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「宵宫」的天赋牌「长野原龙势流星群」的效果：装备此牌后，庭火焰硝的初始可用次数会增加1"
        log[4.7] = "调整了角色牌「宵宫」天赋牌「长野原龙势流星群」所需元素骰和效果：所需元素骰由2个火元素骰调整为1个；装备此牌不会再给宵宫生成的「庭火焰硝」状态初始可用次数+1"
        return log