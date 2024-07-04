from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Collei import * 

class FloralSidewinder(TalentCard):
    id: int = 217011
    name: str = "Floral Sidewinder"
    name_ch = "飞叶迴斜"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 6}]
    cost_power = 0
    character = Collei
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def balance_adjustment():
        log = {}
        log[3.4] = ["调整了「七圣召唤」中天赋牌「飞叶迴斜」所需元素骰子数量：所需骰子数量由3个草元素骰子调整为为4个",
                    "调整了「七圣召唤」中阵营出战状态「激化领域」的可用次数：由3次调整为2次"]
        return log
        