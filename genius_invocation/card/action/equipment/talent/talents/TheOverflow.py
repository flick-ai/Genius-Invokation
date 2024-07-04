from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Candace import *

class TheOverflow(TalentCard):
    id: int = 212071
    name: str = "The Overflow"
    name_ch = "衍溢的汐潮"
    time = 3.8
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 2
    character = Candace
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「坎蒂丝」的天赋牌「衍溢的汐潮」所需元素骰和效果：所需元素骰由4个水元素骰子调整为3个"
        return log
