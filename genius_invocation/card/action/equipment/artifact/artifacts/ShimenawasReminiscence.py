from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class ShimenawasReminiscenceEntity(Artifact):
    name: str = "Shimenawa's Reminiscence"
    name_ch = "追忆之注连"
    max_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.usage = self.max_usage
        self.round = -1

    def update(self):
        self.usage = self.max_usage

    def on_add_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if self.from_character.power >= 2:
                if game.current_damage.damage_type == SkillType.ELEMENTAL_SKILL or  game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    game.current_damage.main_damage += 1

    def on_calculate(self, game:'GeniusGame'):
        if self.round != game.round:
            self.round = game.round
            self.usage = self.max_usage
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == SkillType.ELEMENTAL_SKILL:
                if self.usage > 0:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
                    if len(game.current_dice.cost)>1:
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
            if game.current_dice.use_type == ActionCardType.EQUIPMENT_TALENT:
                 if self.usage > 0:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
                    if game.current_dice.cost[1]['cost_num'] > 0:
                        game.current_dice.cost[1]['cost_num'] -= 1
                        return True
        return False

    def on_skill(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1

    def on_play(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage)
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill),
            (EventType.ON_PLAY_CARD, ZoneType.CHARACTER_ZONE, self.on_play),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate),
        ]


class ShimenawasReminiscence(ArtifactCard):
    id: int = 312014
    name: str = "Shimenawa's Reminiscence"
    name_ch = "追忆之注连"
    cost_num: int = 3
    cost_type: CostType = CostType.BLACK

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = ShimenawasReminiscenceEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

