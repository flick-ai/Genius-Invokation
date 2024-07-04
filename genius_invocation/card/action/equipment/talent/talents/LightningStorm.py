from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Beidou import *

class LightningStorm(TalentCard):
    id: int = 214051
    name: str = "Lightning Storm"
    name_ch = "霹雳连霄"
    time = 3.4
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = Beidou
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.4] = "调整了角色牌「北斗」的天赋牌「霹雳连霄」的效果：现在不再要求角色在准备技能期间受过伤害，即可使北斗本回合内「普通攻击」少花费1个无色元素"
        return log