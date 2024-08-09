from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Cyno import *

class FeatherfallJudgment(TalentCard):
    id: int = 214041
    name: str = "Featherfall Judgment"
    name_ch = "落羽的裁择"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = Cyno
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「赛诺」的天赋牌「落羽的裁择」效果，其伤害增加效果改为：“装备有此牌的赛诺在启途誓使的「凭依」级数为偶数时使用秘仪·律渊渡魂，造成的伤害+1。”"
        log[4.8] = "调整了角色牌「赛诺」天赋牌「落羽的裁择」的效果：效果“装备有此牌的赛诺在启途誓使的「凭依」级数为偶数时，使用秘仪·律渊渡魂造成的伤害+1。”调整为“装备有此牌的赛诺在启途誓使的「凭依」级数至少为2时，使用秘仪·律渊渡魂造成的伤害+2。（每回合1次）”"
        return log
