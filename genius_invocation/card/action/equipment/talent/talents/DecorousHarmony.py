from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Yunjin import *

class DecorousHarmony(TalentCard):
    id: int = 216071
    name: str = "Decorous Harmony"
    name_ch = "庄谐并举"
    time = 4.7
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': CostType.GEO.value}]
    cost_power = 2
    character = Yunjin
    def __init__(self) -> None:
        super().__init__()

    def balance_adjustment():
        log = {}
        log[4.8] = "调整了角色牌「云堇」天赋牌「庄谐并举」的效果：效果“装备有此牌的云堇在场时，如果我方没有手牌，则飞云旗阵会使普通攻击造成的伤害额外+2。”调整为“装备有此牌的云堇在场，且我方触发飞云旗阵时：如果我方没有手牌，则使此次技能伤害+2。”"
        return log
