from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class GoldenTroupesRewardEntity(Artifact):
    name: str =  "Golden Troupe's Reward"
    name_ch = "黄金剧团的奖赏"
    max_usage = 2
    id = 31202591
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.recompense = 0

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            is_use = False
            if game.current_dice.use_type == SkillType.ELEMENTAL_SKILL:
                if game.current_dice.cost[0]['cost_num']>0 and self.usage > 0:
                    new_cost = max(0, game.current_dice.cost[0]['cost_num']-self.recompense)
                    self.recompense = max(0, self.recompense-game.current_dice.cost[0]['cost_num'])
                    game.current_dice.cost[0]['cost_num'] = new_cost
                    is_use = True
                if len(game.current_dice.cost)>1:
                    if game.current_dice.cost[1]['cost_num'] > 0 and self.usage > 0:
                        new_cost = max(0, game.current_dice.cost[1]['cost_num']-self.recompense)
                        self.recompense = max(0, self.recompense-game.current_dice.cost[1]['cost_num'])
                        game.current_dice.cost[1]['cost_num']  = new_cost
                        is_use =  True
            if game.current_dice.use_type == ActionCardType.EQUIPMENT_TALENT:
                if game.current_dice.cost[0]['cost_num']>0 and self.usage > 0:
                    new_cost = max(0, game.current_dice.cost[0]['cost_num']-self.recompense)
                    self.recompense = max(0, self.recompense-game.current_dice.cost[0]['cost_num'])
                    game.current_dice.cost[0]['cost_num'] = new_cost
                    is_use = True
                if len(game.current_dice.cost)>1:
                    if game.current_dice.cost[1]['cost_num'] > 0 and self.usage > 0:
                        new_cost = max(0, game.current_dice.cost[1]['cost_num']-self.recompense)
                        self.recompense = max(0, self.recompense-game.current_dice.cost[1]['cost_num'])
                        game.current_dice.cost[1]['cost_num']  = new_cost
                        is_use =  True
        return is_use

    def on_skill(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1

    def on_play(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1

    def on_end(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if not self.from_character.is_active:
                self.recompense = min(2, self.recompense + 1)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill),
            (EventType.ON_PLAY_CARD, ZoneType.CHARACTER_ZONE, self.on_play),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate),
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end)
        ]



class GoldenTroupesReward(ArtifactCard):
    id: int = 312025
    name: str = "Golden Troupe's Reward"
    name_ch = "黄金剧团的奖赏"
    time = 4.5
    cost_num: int = 0
    cost_type: CostType = None

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = GoldenTroupesRewardEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

