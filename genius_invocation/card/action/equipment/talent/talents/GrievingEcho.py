from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.ThunderManifestation import * 

class GrievingEcho(TalentCard):
    id: int = 224021
    name: str = "Grieving Echo"
    name_ch = "悲号回唱"
    time = 4.3
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = ThunderManifestation
    def __init__(self) -> None:
        super().__init__()

    @staticmethod  
    def balance_adjustment():
        log = {}
        log[4.4] = "调整了角色牌「雷音权现」天赋牌「悲号回唱」所需元素骰，并增加了效果：所需元素骰由0个调整为3个雷元素骰；增加效果“战斗行动：我方出战角色为雷音权现时，装备此牌”，以及“雷音权现装备此牌后，立刻使用一次雷墙倾轧”"
        return log
        