from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Minty_Meat_Rolls_Entity(Status):
    id: int = 33300821
    name: str = "Minty Meat Rolls"
    name_ch = "兽肉薄荷卷"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 3

    def on_calculate(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.from_character == self.from_character:
                if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                    if game.current_dice.cost[1]['cost_num'] > 0:
                        game.current_dice.cost[1]['cost_num'] -= 1
                        return True
        return False

    def on_skill(self, game: 'GeniusGame'):
        if self.on_calculate(game):
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
        ]

class Minty_Meat_Rolls(FoodCard):
    id: int = 333008
    name: str = "Minty Meat Rolls"
    cost_num = 1
    cost_type = CostType.WHITE
    name_ch = "兽肉薄荷卷"

    def __init__(self) -> None:
        super().__init__()
        self.food_entity = Minty_Meat_Rolls_Entity

    def on_played(self, game: 'GeniusGame'):
        super().on_played(game)

    @staticmethod
    def balance_adjustment():
        log = {}
        log[3.4] = "调整了「七圣召唤」中事件牌「兽肉薄荷卷」的效果：现在其效果最多能触发3次”"
        return log

