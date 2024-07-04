from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Xingqiu import *

class TheScentRemained(TalentCard):
    id: int = 212021
    name: str = "The Scent Remained"
    name_ch = "重帘留香"
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 0
    character = Xingqiu
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「行秋」的天赋牌「重帘留香」所需元素骰和效果：所需元素骰由4个水元素骰子调整为3个；装备该天赋牌后，雨帘剑会在我方出战角色受到至少为2的伤害时抵消伤害"
        return log
