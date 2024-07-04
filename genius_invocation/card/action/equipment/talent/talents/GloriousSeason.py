from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Barbara import *

class GloriousSeason(TalentCard):
    id: int = 212011
    name: str = "Glorious Season"
    name_ch = "光辉的季节"
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 0
    character = Barbara
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「芭芭拉」的天赋牌「光辉的季节」所需元素骰：所需元素骰由4个水元素骰子调整为3个"
        return log
