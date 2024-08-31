from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class SaurusCrackersEntity(Status):
    id: int = 33301621
    name: str = "Saurus Crackers"
    name_ch = "龙龙饼干"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def on_calculate(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.from_character == self.from_character:
                if game.current_dice.use_type == SpecialSkillType.SPECIAL_SKILL:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
        return False

    def on_special_skill(self, game: 'GeniusGame'):
        if self.on_calculate(game):
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def on_end(self, game: 'GeniusGame'):
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_USE_SPECIAL, ZoneType.CHARACTER_ZONE, self.on_special_skill),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end)
        ]

class SaurusCrackers(FoodCard):
    id: int = 333016
    name: str = "Saurus Crackers"
    name_ch = "龙龙饼干"
    time = 5.1
    cost_num = 0
    cost_type = None

    def __init__(self) -> None:
        super().__init__()
        self.food_entity = SaurusCrackersEntity

    def on_played(self, game: 'GeniusGame'):
        super().on_played(game)

