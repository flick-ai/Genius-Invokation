from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Zhongli import *

class DominanceofEarth(TalentCard):
    id: int = 216031
    name: str = "Dominance of Earth"
    name_ch = "炊金馔玉"
    time = 3.7
    is_action = True
    cost = [{'cost_num': 5, 'cost_type': 5}]
    cost_power = 0
    character = Zhongli
    def __init__(self) -> None:
        super().__init__()

    def balance_adjustment():
        log = {}
        log[4.8] = "调整了角色牌「钟离」天赋牌「炊金馔玉」的效果：效果“我方出战角色在护盾角色状态或护盾出战状态的保护下时，我方召唤物造成的岩元素伤害+1。”调整为“装备有此牌的钟离生命值至少为7时，钟离造成的伤害和我方召唤物造成的岩元素伤害+1。”"
        return log

