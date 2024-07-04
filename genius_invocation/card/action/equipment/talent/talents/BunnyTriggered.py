from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Amber import *

class BunnyTriggered(TalentCard):
    id: int = 213041
    name: str = "Bunny Triggered"
    name_ch = "一触即发"
    time = 3.7
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 2}]
    cost_power = 0
    character = Amber
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「安柏」的天赋牌「一触即发」引爆兔兔伯爵的伤害：由3点火元素伤害调整为4点"
        return log
