from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Diluc import * 

class FlowingFlame(TalentCard):
    id: int = 213011
    name: str = "Flowing Flame"
    name_ch = "流火焦灼"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 2}]
    cost_power = 0
    character = Diluc
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.7] = "调整了角色牌「迪卢克」天赋牌「流火焦灼」的效果：现在装备此牌的迪卢克，每回合第2次、第3次使用「逆焰之刃」时都会受到“少花费1个火元素骰”的效果（原仅限“每回合第2次使用「逆焰之刃」”）"
      

        