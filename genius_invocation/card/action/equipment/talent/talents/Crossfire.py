from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Xiangling import *

class Crossfire(TalentCard):
    id: int = 213021
    name: str = "Crossfire"
    name_ch = "交叉火力"
    is_action = True
    # 4.2更新
    cost = [{'cost_num': 3, 'cost_type': 2}]
    cost_power = 0
    character = Xiangling
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「香菱」的天赋牌「交叉火力」所需元素骰：所需元素骰由4个火元素骰子调整为3个"
        return log
