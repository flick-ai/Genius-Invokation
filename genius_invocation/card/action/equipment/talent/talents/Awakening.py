from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Razor import *

class Awakening(TalentCard):
    id: int = 214021
    name: str = "Awakening"
    name_ch = "觉醒"
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = Razor
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「雷泽」的天赋牌「觉醒」所需元素骰和效果：所需元素骰由4个雷元素骰子调整为3个；“使我方一个雷元素角色获得1点充能。”的效果现在每回合可触发1次"
        return log
