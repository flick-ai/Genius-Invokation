from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Lotus_Flower_Crisp_Entity(Status):
    id: int = 33300321
    name: str = "Lotus Flower Crisp"
    name_ch = "莲花酥"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.on_destroy(game)

    def on_damage_execute(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PIERCING:
                return
            if game.current_damage.main_damage > 0:
                game.current_damage.main_damage = max(0, game.current_damage.main_damage-3)
                self.current_usage -=1
                if self.current_usage <=0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_damage_execute),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
        ]

class Lotus_Flower_Crisp(FoodCard):
    id: int = 333003
    name: str = "Lotus Flower Crisp"
    name_ch = "莲花酥"
    cost_num = 1
    cost_type = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.food_entity = Lotus_Flower_Crisp_Entity

    def on_played(self, game: 'GeniusGame'):
        super().on_played(game)

