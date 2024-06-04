from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Combat_Status
from genius_invocation.utils import *

import os
import random

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class Sunyata_Flower_Entity(Combat_Status):
    name: str = 'Sunyata Flower'
    name_ch = '净觉花'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type in [ActionCardType.SUPPORT_ITEM,
                                              ActionCardType.SUPPORT_LOCATION,
                                              ActionCardType.SUPPORT_COMPANION,]:
                if game.current_dice.cost[0]['cost_num'] > 0:
                    game.current_dice.cost[0]['cost_num'] = max(0, game.current_dice.cost[0]['cost_num']-1)
                    return True
        return False

    def on_play(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.on_destroy(game)

    def on_end(self, game: 'GeniusGame'):
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_PLAY_CARD, ZoneType.ACTIVE_ZONE, self.on_play),
            (EventType.CALCULATE_DICE, ZoneType.ACTIVE_ZONE, self.on_calculate),
            (EventType.FINAL_END, ZoneType.ACTIVE_ZONE, self.on_end),
        ]

class Sunyata_Flower(ActionCard):
    id: int = 332029
    name: str = 'Sunyata Flower'
    name_ch = '净觉花'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()
        cards_dirs = ["./card/action/support/companion",
                      "./card/action/support/item",
                      "./card/action/support/location"]
        self.cards = []
        for package_dir in cards_dirs:
            available_name = [f[:-3] for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
            self.cards.extend(available_name)

    def on_played(self, game: 'GeniusGame'):
        target = game.current_action.target_idx
        game.active_player.support_zone.destroy_by_idx(target)
        card_name = random.choice(self.cards)
        game.active_player.hand_zone.add_card_by_name(card_name)

    def find_target(self, game: 'GeniusGame'):
        if game.active_player.support_zone.num() > 0:
            target = []
            for idx, support in enumerate(game.active_player.support_zone.space):
                target.append(idx+9)
            return target
        else:
            return []
