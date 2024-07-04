from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Furina import *

class HearMe(TalentCard):
    id: int = 212111
    name: str = "Hear Me — Let Us Raise the Chalice of Love!"
    name_ch = "「诸君听我颂，共举爱之杯！」"
    time = 4.7
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': CostType.HYDRO.value}]
    cost_power = 0
    character = Furina
    def __init__(self) -> None:
        super().__init__()
