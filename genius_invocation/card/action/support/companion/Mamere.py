from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support
from genius_invocation.entity.status import Status

import random
import os

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Mamere_Entity(Support):
    id: int = 322021
    name: str = 'Mamere'
    name_ch = '玛梅赫'
    max_usage = 3
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.usage_round = -1
        cards_dirs = ["./card/action/support/companion",
                      "./card/action/support/item",
                      "./card/action/support/location",
                      "./card/action/event/foods"]
        self.cards = []
        for package_dir in cards_dirs:
            available_name = [f[:-3] for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
            self.cards.extend(available_name)

    def on_play_card(self, game:'GeniusGame'):
        if self.usage_round != game.round:
            if game.current_card.card_type in [ActionCardType.SUPPORT_COMPANION,
                                               ActionCardType.SUPPORT_LOCATION,
                                               ActionCardType.SUPPORT_ITEM,
                                               ActionCardType.EVENT_FOOD] \
                and game.current_card.name != 'Mamere':

                self.usage_round = game.round
                self.usage -= 1
                card_name = random.choice(self.cards)
                self.from_player.hand_zone.add_card_by_name(card_name)
                if self.usage <= 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play_card),
        ]

    def show(self):
        return str(self.sophistication)


class Mamere(SupportCard):
    id: int = 322021
    name: str = 'Mamere'
    name_ch = '玛梅赫'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Mamere_Entity(game, from_player=game.active_player)
        super().on_played(game)

if __name__ == "__main__":
    cards_dirs = ["./card/action/support/companion",
                      "./card/action/support/item",
                      "./card/action/support/location",
                      "./card/action/event/foods"]
    for package_dir in cards_dirs:
        available_name = [f[:-3] for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
        print(package_dir, available_name)