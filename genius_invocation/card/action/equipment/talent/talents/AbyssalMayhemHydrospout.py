from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Tartaglia import *

class AbyssalMayhemHydrospout(TalentCard):
    id: int = 212041
    name: str = "Abyssal Mayhem: Hydrospout"
    name_ch = "深渊之灾·凝水盛放"
    time = 3.7
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 0
    character = Tartaglia
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.1] = "调整了角色牌「达达利亚」天赋牌「深渊之灾·凝水盛放」所需元素骰费用和效果：所需元素骰调整为3个水元素骰；结束阶段现在会对附属有「断流」的出战角色造成1点穿透伤害"
        return log