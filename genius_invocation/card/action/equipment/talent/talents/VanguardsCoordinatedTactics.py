from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Chevreuse import *

class VanguardsCoordinatedTactics(TalentCard):
    id: int = 213131
    name: str = "Vanguard's Coordinated Tactics"
    name_ch = "尖兵协同战法"
    time = 4.8
    is_action = False
    cost = [{'cost_num': 2, 'cost_type': CostType.PYRO.value}]
    cost_power = 0
    character = Chevreuse
    def __init__(self) -> None:
        super().__init__()

    def find_target(self, game: 'GeniusGame'):
        for idx, character in enumerate(game.active_player.character_list):
            if isinstance(character, self.character):
                if character.is_alive:
                    unique_element_set = character.from_player.element_set
                    if len(unique_element_set) == 2 and ElementType.PYRO in unique_element_set and ElementType.ELECTRO in unique_element_set:
                        return [idx+2]
        return []
