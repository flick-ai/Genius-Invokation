from genius_invocation.utils import *
from genius_invocation.card.action.equipment.base import EquipmentCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import SpecialSkill
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class SpecialSkillCard(EquipmentCard):
    name: str
    equipment_entity: 'SpecialSkill'
    card_type = ActionCardType.EQUIPMENT_SPECIAL_SKILL
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        idx = game.current_action.target_idx
        target_character = game.active_player.character_list[idx]
        entity = self.equipment_entity(game,
                                       game.active_player,
                                       target_character)
        if target_character.character_zone.special_skill != None:
            target_character.character_zone.special_skill.on_destroy(game)
        target_character.character_zone.special_skill = entity

    def find_target(self, game: 'GeniusGame'):
        character_idx = []
        for idx, character in enumerate(game.active_player.character_list):
            if character.is_alive:
                character_idx.append(idx + 2)
        return character_idx

    def on_tuning(self, game: 'GeniusGame'):
        return super().on_tuning(game)