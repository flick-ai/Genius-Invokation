from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Jueyun_Guoba_Entity(Status):
    id: int = 333001
    name: str = 'Jueyun Guoba'
    
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
    
    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                game.current_damage.main_damage += 1
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

class Jueyun_Guoba(FoodCard):
    id: int = 333001
    name: str = 'Jueyun Guoba'
    cost_num = 0
    cost_type = None

    def __init__(self) -> None:
        super().__init__()
        self.food_entity = Jueyun_Guoba_Entity

    def on_played(self, game: 'GeniusGame'):
        super().on_played(game)

    