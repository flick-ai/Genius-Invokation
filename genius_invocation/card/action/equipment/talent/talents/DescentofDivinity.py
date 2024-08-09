from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Albedo import *

class DescentofDivinity(TalentCard):
    id: int = 216041
    name: str = "Descent of Divinity"
    name_ch = "神性之陨"
    time = 4.0
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 5}]
    cost_power = 0
    character = Albedo
    def __init__(self) -> None:
        super().__init__()

    def balance_adjustment(self):
        log = {}
        log[4.8] = " 调整了角色牌「阿贝多」天赋牌「神性之陨」的效果：“装备有此牌的阿贝多在场时，如果我方场上存在阳华，则我方角色进行下落攻击时造成的伤害+1。”增加了效果“进行下落攻击时少花费1个无色元素”"
        return log
