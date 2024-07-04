from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.AbyssLectorFathomlessFlames import * 

class EmbersRekindled(TalentCard):
    id: int = 223021
    name: str = "Embers Rekindled"
    name_ch = "烬火重燃"
    is_action = False
    cost = [{'cost_num': 2, 'cost_type': 2}]
    cost_power = 0
    character = AbyssLectorFathomlessFlames
    time = 3.7
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.6] = "调整了角色牌「深渊咏者·渊火」天赋牌「烬火重燃」附属的「渊火加护」效果：效果调整为：“为所附属角色提供2点护盾。此护盾耗尽后：对所有敌方角色造成1点穿透伤害”"
        return log
        