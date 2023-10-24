from genius_invocation.utils import *
from genius_invocation.card.action.equipment.base import EquipmentCard
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.entity.status import Artifact

class ArtifactCard(EquipmentCard):
    # 圣遗物牌
    artifact_entity: 'Artifact'
    card_type = ActionCardType.EQUIPMENT_ARTIFACT
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        idx = game.current_action.target_idx
        target_character = game.active_player.character_list[idx]
        entity = self.artifact_entity(game=game,
                                       from_player=game.active_player,
                                       from_character=target_character,
                                       artifact_card=self)
        if target_character.character_zone.artifact_card != None:
            target_character.character_zone.artifact_card.on_destroy(game)
        target_character.character_zone.artifact_card = entity

    def find_target(self, game: 'GeniusGame'):
        character_idx = []
        for idx, character in enumerate(game.active_player.character_list):
            if character.is_alive:
                character_idx.append(idx + 2)
        return character_idx

    def on_tuning(self, game: 'GeniusGame'):
        return super().on_tuning(game)
