from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.MirrorMaiden import *

class MirrorCage(TalentCard):
    id: int = 222021
    name: str = "Mirror Cage"
    name_ch = "镜锢之笼"
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 0
    character = MirrorMaiden
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「愚人众·藏镜仕女」的天赋牌「镜锢之笼」所需元素骰：所需元素骰由4个水元素骰子调整为3个"
        log[4.8] = "调整了角色牌「藏镜仕女」天赋牌「镜锢之笼」的效果：效果“并且会使所附属角色切换到其他角色时元素骰费用+1”调整为“并且会使附属角色受到的水元素伤害+1”"
        return log
