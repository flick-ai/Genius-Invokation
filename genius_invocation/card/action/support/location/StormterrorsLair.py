from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class StormterrorsLairEntity(Support):
    name: str = "Stormterror's Lair"
    name_ch = '风龙废墟'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        card = self.from_player.card_zone.random_find_card(card_type=ActionCardType.EQUIPMENT_TALENT, num=1)
        self.from_player.hand_zone.add(card)
        self.usage_round = -1
        self.usage = 1

    def on_calculate(self, game:'GeniusGame'):
        if game.round != self.usage_round:
            self.usage_round = game.round
            self.usage = 1
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type in SkillType:
                if self.usage > 0:
                    if game.current_dice.origin_cost[0]['cost_num'] > 4:
                        game.current_dice.cost[0]['cost_num'] -= 1
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
            (EventType.ON_USE_SKILL, ZoneType.SUPPORT_ZONE, self.on_skill),
            (EventType.ON_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play),
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
        ]

    def show(self):
        if self.usage>0:
            return '┬─┬┬─┬'
        else:
            return '(╯°□°）╯︵ ┻━┻┻━┻'

class StormterrorsLair(SupportCard):
    id: int = 321015
    name: str = "Stormterror's Lair"
    name_ch = '风龙废墟'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = StormterrorsLairEntity(game, from_player=game.active_player)
        super().on_played(game)