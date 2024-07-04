from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Yanfei import *

class RightofFinalInterpretation(TalentCard):
    id: int = 213081
    name: str = "Right of Final Interpretation"
    name_ch = "最终解释权"
    time = 3.8
    is_action = True
    cost = [{'cost_num': 1, 'cost_type': 2}, {'cost_num': 2, 'cost_type': 8}]
    cost_power = 0
    character = Yanfei
    def __init__(self) -> None:
        super().__init__()
