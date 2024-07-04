from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.SangonomiyaKokomi import * 

class TamakushiCasket(TalentCard):
    id: int = 212051
    name: str = "Tamakushi Casket"
    name_ch = "匣中玉栉"
    time = 3.5
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 2
    character = SangonomiyaKokomi
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「珊瑚宫心海」的天赋牌「匣中玉栉」效果：如果化海月在场，则将其可用次数加1；若场上不存在化海月，则召唤一个可用次数为1的化海月"
        return log
        