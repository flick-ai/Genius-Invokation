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
    cost_power: int = 0
    skill_idx: int
    character: Type
    def __init__(self) -> None:
        super().__init__()
        
    def on_played(self, game: 'GeniusGame') -> None:
        target_character = game.active_player.character_list[game.current_action.target_idx]
        target_character.talent = True
        if self.is_action:
            target_character.skills[self.skill_idx].on_call(game)

    def find_target(self, game: 'GeniusGame'):
        if not self.is_action:
            for idx, character in enumerate(game.active_player.character_list):
                if isinstance(character, self.character):
                    return [idx+2]
        else:
            if isinstance(get_my_active_character(game), self.character):
                if get_my_active_character(game).power >= self.cost_power:
                    return [game.active_player.active_idx+2]
        return []