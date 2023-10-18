from utils import *
from typing import TYPE_CHECKING

# from utils import GeniusGame
from ..base import EquipmentCard
# from entity.entity import Entity

if TYPE_CHECKING:
    from game.game import GeniusGame
    from entity.status import Weapon



class WeaponCard(EquipmentCard):
    # 武器牌
    weapon_type:'WeaponType'
    equipment_entity: 'Weapon'
    def __init__(self) -> None:
        super().__init__()
        self.card_type = ActionCardType.EQUIPMENT_WEAPON


    def on_played(self, game: 'GeniusGame') -> None:
        idx = game.current_action.target_idx
        target_character = game.active_player.character_list[idx]
        entity = self.equipment_entity(game=game,
                                       from_player=game.active_player,
                                       from_character=target_character,
                                       weapon_card=self)
        target_character.character_zone.weapon_card = entity
    
    def find_target(self, game: 'GeniusGame'):
        character_idx = []
        for idx, character in enumerate(game.active_player.character_list):
            if character.is_alive and character.character_zone.weapon_card is None:
                if character.weapon_type == self.weapon_type:
                    character_idx.append(idx + 2)
        return character_idx
    
    def on_tuning(self, game: 'GeniusGame'):
        return super().on_tuning(game)