from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.MaguuKenki import *

class TranscendentAutomaton(TalentCard):
    id: int = 225011
    name: str = "Transcendent Automaton"
    name_ch = "机巧神通"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 4}]
    cost_power = 0
    character = MaguuKenki
    def __init__(self) -> None:
        super().__init__()
