from genius_invocation.utils import *
from genius_invocation.card.action.equipment.base import EquipmentCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Artifact
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

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
    
class SmallElement(Artifact):
    # 小元素圣遗物
    max_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.usage = self.max_usage
        self.round = -1

    def update(self):
        self.usage = self.max_usage

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type in SkillType:
                if self.usage > 0:
                    if game.current_dice.cost[0]['cost_num'] > 0 and game.current_dice.cost[0]['cost_type']==self.element_type:
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
                    if game.current_dice.cost[1]['cost_num'] > 0 and game.current_dice.cost[0]['cost_type']==self.element_type:
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
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill),
            (EventType.ON_PLAY_CARD, ZoneType.CHARACTER_ZONE, self.on_play),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate),
        ]

class BigElement(Artifact):
    # 大元素圣遗物
    max_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.usage = self.max_usage
        self.round = -1

    def update(self):
        self.usage = self.max_usage
    
    def on_roll(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            dice_type = CostToDice[self.element_type]
            self.from_player.fix_dice += [dice_type.value, dice_type.value,]

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type in SkillType:
                if self.usage > 0:
                    if game.current_dice.cost[0]['cost_num'] > 0 and game.current_dice.cost[0]['cost_type']==self.element_type:
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
                    if game.current_dice.cost[1]['cost_num'] > 0 and game.current_dice.cost[0]['cost_type']==self.element_type:
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
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill),
            (EventType.ON_PLAY_CARD, ZoneType.CHARACTER_ZONE, self.on_play),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate),
            (EventType.BEGIN_ROLL_PHASE, ZoneType.CHARACTER_ZONE, self.on_roll)
        ]