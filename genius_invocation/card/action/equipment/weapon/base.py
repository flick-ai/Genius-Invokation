from genius_invocation.utils import *
from typing import TYPE_CHECKING

# from genius_invocation.utils import GeniusGame
from genius_invocation.card.action.equipment.base import EquipmentCard
# from genius_invocation.entity.entity import Entity

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.entity.status import Weapon



class WeaponCard(EquipmentCard):
    # 武器牌
    weapon_type:'WeaponType'
    equipment_entity: 'Weapon'
    card_type = ActionCardType.EQUIPMENT_WEAPON
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
        if target_character.character_zone.weapon_card != None:
            target_character.character_zone.weapon_card.on_destroy(game)
        target_character.character_zone.weapon_card = entity

    def find_target(self, game: 'GeniusGame'):
        character_idx = []
        for idx, character in enumerate(game.active_player.character_list):
            if character.is_alive:
                if character.weapon_type == self.weapon_type:
                    character_idx.append(idx + 2)
        return character_idx

    def on_tuning(self, game: 'GeniusGame'):
        return super().on_tuning(game)