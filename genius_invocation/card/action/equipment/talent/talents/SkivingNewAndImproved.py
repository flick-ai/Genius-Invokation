from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Sayu import *

class SkivingNewAndImproved(TalentCard):
    id: int = 215071
    name: str = "Skiving: New and Improved"
    name_ch = "偷懒的新方法"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 4}]
    cost_power = 0
    character = Sayu
    def __init__(self) -> None:
        super().__init__()

