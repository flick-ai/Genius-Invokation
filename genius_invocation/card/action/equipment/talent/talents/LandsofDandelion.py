from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Jean import *

class LandsofDandelion(TalentCard):
    id: int = 215021
    name: str = "Lands of Dandelion"
    name_ch = "蒲公英的国土"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 4}]
    cost_power = 2
    character = Jean
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「琴」的天赋牌「蒲公英的国土」所需充能：所需充能由3调整为2"
        return log
