from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.ElectroHypostasis import ElectroHypostasis

class AbsorbingPrism(TalentCard):
    id: int = 224011
    name: str = "Absorbing Prism"
    name_ch = "汲能棱晶"
    time = 3.7
    is_action = True
    card_type = ActionCardType.EVENT
    # 4.2更新
    cost = [{'cost_num': 2, 'cost_type': 3}]
    cost_power = 0
    character = ElectroHypostasis
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了角色牌「雷电法则」的天赋牌「汲能棱晶」所需元素骰：所需元素骰由3个雷元素骰子调整为2个"
        return log

