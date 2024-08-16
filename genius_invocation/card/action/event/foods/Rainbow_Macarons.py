from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Rainbow_Macarons_Entity(Status):
    id: int = 33301521
    name: str = "Rainbow Macarons"
    name_ch = "缤纷马卡龙"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.from_character.heal(heal=1,game=game)
        self.current_usage = 3
        self.is_heal = False

    def on_excute(self, game: 'GeniusGame'):
        if self.is_heal:
            self.is_heal = False
            self.from_character.heal(heal=1, game=game)
            self.current_usage -= 1
            if self.current_usage <=0:
                self.on_destroy(game)

    def on_damage(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            self.is_heal = True

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_damage),
            (EventType.FINAL_EXECUTE, ZoneType.CHARACTER_ZONE, self.on_damage),
        ]

class Rainbow_Macarons(FoodCard):
    id: int = 333015
    name: str = "Rainbow Macarons"
    cost_num = 2
    cost_type = CostType.BLACK
    name_ch = "缤纷马卡龙"
    time = 4.6

    def __init__(self) -> None:
        super().__init__()


    def on_played(self, game: 'GeniusGame'):
        super().on_played(game)
        self.food_entity = Rainbow_Macarons_Entity

    def find_target(self, game: 'GeniusGame'):
        target_list = []
        for idx, character in enumerate(game.active_player.character_list):
            if not character.is_satisfy and character.health_point != character.max_health_point:
                target_list.append(idx+2)
        return target_list


