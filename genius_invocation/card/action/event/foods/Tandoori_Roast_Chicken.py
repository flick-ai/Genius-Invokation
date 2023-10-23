from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Tandoori_Roast_Chicken_Entity(Status):
    id: int = 333011
    name: str = "Tandoori Roast Chicken"
    name_ch = "唐杜尔烤鸡"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
    
    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.ELEMENTAL_SKILL:
                game.current_damage.main_damage += 2
                self.current_usage -= 1
                if self.current_usage == 0:
                    self.on_destroy(game)

    def on_begin(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
        ]

class Tandoori_Roast_Chicken(FoodCard):
    id: int = 333011
    name: str = "Tandoori Roast Chicken"
    name_ch = "唐杜尔烤鸡"
    cost_num = 2
    cost_type = CostType.BLACK

    def __init__(self) -> None:
        super().__init__()
        self.food_entity = Tandoori_Roast_Chicken_Entity

    def on_played(self, game: 'GeniusGame'):
        super().on_played(game)
    
    def find_target(self, game: 'GeniusGame'):
        return [1]

    