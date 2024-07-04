from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.KamisatoAyato import *

class KyoukaFuushi(TalentCard):
    id: int = 212061
    name: str = "Kyouka Fuushi"
    name_ch = "镜华风姿"
    time = 3.6
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 0
    character = KamisatoAyato
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.1] = "调整了角色牌「神里绫人」所需元素骰费用和技能伤害：元素战技附属的「泷廻鉴花」状态可用次数调整为3；元素爆发所需充能调整为2，造成的水元素伤害调整为1"
        log[4.7] = "调整了角色牌「神里绫人」天赋牌「镜华风姿」的效果：“对于生命值不多于6的敌人”的“伤害额外+1”效果改为“伤害额外+2”"
        return log