from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Yanfei import *

class RightofFinalInterpretation(TalentCard):
    id: int = 213081
    name: str = "Right of Final Interpretation"
    name_ch = "最终解释权"
    time = 3.8
    is_action = True
    cost = [{'cost_num': 1, 'cost_type': 2}, {'cost_num': 2, 'cost_type': 8}]
    cost_power = 0
    character = Yanfei
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「烟绯」的天赋牌「最终解释权」的效果，调整为：“装备有此牌的烟绯进行重击时：对生命值不多于6的敌人造成的伤害+1；如果触发了丹火印，则在技能结算后抓一张牌”"
        return log
