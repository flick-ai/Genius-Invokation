from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Shougun import * 

class WishesUnnumbered(TalentCard):
    id: int = 214071
    name: str = "Wishes Unnumbered"
    name_ch = "万千的愿望"
    is_action = True
    cost = [{'cost_num': 4, 'cost_type': 3}]
    cost_power = 2
    character = Shougun
    def __init__(self) -> None:
        super().__init__()
        