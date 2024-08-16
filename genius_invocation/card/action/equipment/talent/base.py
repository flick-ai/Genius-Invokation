from genius_invocation.utils import *
from genius_invocation.card.action.equipment.base import EquipmentCard
from typing import Type
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.zone import CharacterZone
    from genius_invocation.game.player import GeniusPlayer



class TalentCard(EquipmentCard):
    '''
        天赋牌
    '''
    card_type = ActionCardType.EQUIPMENT_TALENT
    is_action: bool = True
    is_equip: bool = True
    cost_power: int = 0
    character: Type
    cost: list[dict]
    def __init__(self) -> None:
        super().__init__()
        for i in range(len(self.cost)):
            self.cost[i]['cost_type'] = CostType(self.cost[i]['cost_type'])

    def on_played(self, game: 'GeniusGame') -> None:
        target_character = game.active_player.character_list[game.current_action.target_idx]
        target_character.equip_talent(game, self.is_action, self)

    def find_target(self, game: 'GeniusGame'):
        if not self.is_action:
            for idx, character in enumerate(game.active_player.character_list):
                if isinstance(character, self.character):
                    if character.is_alive:
                        return [idx+2]
        else:
            if isinstance(get_my_active_character(game), self.character):
                if get_my_active_character(game).power >= self.cost_power:
                    return [game.active_player.active_idx+2]
        return []

    def count_cost(self):
        if self.is_equip:
            return sum([cost['cost_num'] for cost in self.cost])
        else:
            return 0