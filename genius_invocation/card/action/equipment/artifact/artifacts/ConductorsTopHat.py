from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class ConductorsTopHatEntity(Artifact):
    name: str =  "Conductor's Top Hat"
    name_ch = "指挥的礼帽"
    id = 31203091
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.round_usage = 1
        self.is_excute = False

    def on_change_character(self, game: 'GeniusGame'):
        if game.current_switch.to_character == self.from_character:
            if self.round_usage > 0:
                self.is_excute = True
                player = self.from_character.from_player
                max_id = max_count_card(player.hand_zone.card)
                player.hand_zone.discard_card(max_id)
                num = self.from_player.dice_zone.num()
                self.from_player.dice_zone.remove([num-2, num-1])
                self.from_player.dice_zone.add([DiceType.OMNI for _ in range(2)])
                self.round_usage -= 1

    def on_calculate_dice(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.is_excute:
                if game.current_dice.use_type in SkillType:
                    if self.round_usage > 0:
                        if game.current_dice.cost[0]['cost_num'] > 0:
                            game.current_dice.cost[0]['cost_num'] -= 1
                            return True
                        if len(game.current_dice.cost)>1:
                            if game.current_dice.cost[1]['cost_num'] > 0:
                                game.current_dice.cost[1]['cost_num'] -= 1
                                return True
                if game.current_dice.use_type == ActionCardType.EQUIPMENT_TALENT:
                    if self.round_usage > 0:
                        if game.current_dice.cost[0]['cost_num'] > 0:
                            game.current_dice.cost[0]['cost_num'] -= 1
                            return True
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
        return False

    def on_use_skill(self, game: 'GeniusGame'):
        if self.on_calculate_dice(game):
            self.is_excute = False

    def on_play_card(self, game: 'GeniusGame'):
        if self.on_calculate_dice(game):
            self.is_excute = False

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_PLAY_CARD, ZoneType.CHARACTER_ZONE, self.on_change_character),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_use_skill),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice),
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_change_character),
        ]


class ConductorsTopHat(ArtifactCard):
    id: int = 312030
    name: str = "Marechaussee Hunter"
    name_ch = "指挥的礼帽"
    time = 5.1
    cost_num: int = 1
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = ConductorsTopHatEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

