from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Fish_and_Chips_Entity(Status):
    id: int = 333013
    name: str = "Fish and Chips"
    name_ch = "炸鱼薯条"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type in SkillType:
                if self.usage > 0:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
                    if len(game.current_dice.cost)>1:
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
        return False

    def on_skill(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.on_destroy(game)

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_USE_SKILL, ZoneType.SUPPORT_ZONE, self.on_skill),
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]
class Fish_and_Chips(FoodCard):
    id: int = 333013
    name: str = "Fish and Chips"
    name_ch = "炸鱼薯条"
    cost_num = 2
    cost_type = CostType.BLACK

    def __init__(self) -> None:
        super().__init__()
        self.food_entity = Fish_and_Chips_Entity

    def on_played(self, game: 'GeniusGame'):
        super().on_played(game)

    def find_target(self, game: 'GeniusGame'):
        flag = True
        for _, character in enumerate(game.active_player.character_list):
            if character.is_alive and character.is_satisfy:
                flag = False
                break
        if flag:
            return [1]
        return []

