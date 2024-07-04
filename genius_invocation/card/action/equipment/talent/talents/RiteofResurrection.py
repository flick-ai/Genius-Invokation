from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Qiqi import * 

class RiteofResurrection(TalentCard):
    id: int = 211081
    name: str = "Rite of Resurrection"
    name_ch = "起死回骸"
    time = 4.0
    is_action = True
    # 4.7平衡性调整：费用5变为4
    cost = [{'cost_num': 5, 'cost_type': CostType.CRYO.value}]
    cost_power = 3
    character = Qiqi
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.7] = "调整了角色牌「七七」天赋牌「起死回骸」所需元素骰：所需元素骰由5个冰元素骰改为4个"
        return log