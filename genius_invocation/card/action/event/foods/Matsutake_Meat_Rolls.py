from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Matsutake_Meat_Rolls_Entity(Status):
    id: int = 333014
    name: str = "Matsutake Meat Rolls"
    name_ch = "松茸酿肉卷"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.from_character.heal(heal=2,game=game)
        self.current_usage = 3

    def on_end(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.from_character.heal(heal=1,game=game)
            self.current_usage -= 1
            if self.current_usage <=0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end),
        ]

class Matsutake_Meat_Rolls(FoodCard):
    id: int = 333014
    name: str = "Matsutake Meat Rolls"
    cost_num = 2
    cost_type = CostType.WHITE
    name_ch = "松茸酿肉卷"
    time = 4.4

    def __init__(self) -> None:
        super().__init__()


    def on_played(self, game: 'GeniusGame'):
        super().on_played(game)
        self.food_entity = Matsutake_Meat_Rolls_Entity

    def find_target(self, game: 'GeniusGame'):
        target_list = []
        for idx, character in enumerate(game.active_player.character_list):
            if not character.is_satisfy and character.health_point != character.max_health_point:
                target_list.append(idx+2)
        return target_list


