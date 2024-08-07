from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Chongyun import *

class SteadyBreathing(TalentCard):
    id: int = 211041
    name: str = "Steady Breathing"
    name_ch = "吐纳真定"
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 0}]
    cost_power = 0
    character = Chongyun
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「重云」的天赋牌「吐纳真定」所需元素骰和效果：所需元素骰由4个冰元素骰子调整为3个，并移除了使重华叠霜领域“初始持续回合+1”的效果"
        return log
