from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class KusavaEntity(Support):
    name: str = 'Kusava'
    name_ch = '苦舍桓'
    max_count = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.memories_and_dreams = 0

    def get_max_count_card(self, game: 'GeniusGame'):
        max_count = 0
        max_idx = []
        for idx, action_card in enumerate(self.from_player.hand_zone.card):
            if action_card.card_type == ActionCardType.EQUIPMENT_TALENT:
                count = sum([i['cost_num'] for i in action_card.cost])
            else:
                count = action_card.cost_num

            if count > max_count:
                max_idx = []
                max_count = count
                max_idx.append(idx)
            if count == max_count:
                max_idx.append(idx)
        return idx

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            max_count_idx = self.get_max_count_card(game)
            if len(max_count_idx) == 0:
                return
            if len(max_count_idx) > 2:
                max_count_idx = max_count_idx[0:2]

            for idx in max_count_idx:
                self.from_player.hand_zone.discard_card(idx)
                self.memories_and_dreams = min(self.max_count, self.memories_and_dreams + 1)

    def on_calculate_dice(self, game: 'GeniusGame') -> bool:
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type in SkillType:
                if self.from_player.round_play_cards == 0:
                    if self.memories_and_dreams > 0:
                        if game.current_dice.cost[0]['cost_num'] > 0:
                            game.current_dice.cost[0]['cost_num'] -= 1
                            return True
                        if len(game.current_dice.cost) > 1:
                            if game.current_dice.cost[1]['cost_num'] > 0:
                                game.current_dice.cost[1]['cost_num'] -= 1
                                return True
        return False

    def on_skill(self, game: 'GeniusGame') -> None:
        if self.on_calculate_dice(game):
            self.memories_and_dreams -= 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_USE_SKILL, ZoneType.SUPPORT_ZONE, self.on_skill),
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate_dice),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]
    def show(self):
        return str(self.usage)

class Kusava(SupportCard):
    id: int = 323008
    name: str = 'Kusava'
    name_ch = '苦舍桓'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_ITEM

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = KusavaEntity(game, from_player=game.active_player)
        super().on_played(game)
