from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.KujouSara import *

class SinofPride(TalentCard):
    id: int = 214061
    name: str = "Sin of Pride"
    name_ch = "我界"
    time = 3.5
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = KujouSara
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「九条裟罗」的天赋牌「我界」所需元素骰和效果：所需元素骰由4个雷元素骰子调整为3个，不再需要充能；九条裟罗装备此牌后，不会再使用煌煌千道镇式，改为立刻使用一次鸦羽天狗霆雷召咒"
        return log
