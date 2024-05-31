from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Butter_Crab_Entity(Status):
    id: int = 333012
    name: str = "Butter_Crab"
    name_ch = "黄油蟹蟹"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def on_damage_execute(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PIERCING:
                return
            if game.current_damage.main_damage > 0:
                game.current_damage.main_damage = max(0, game.current_damage.main_damage-2)
                self.current_usage -=1
                if self.current_usage <=0:
                    self.on_destroy(game)

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_damage_execute),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
        ]

class Butter_Crab(FoodCard):
    id: int = 333012
    name: str = "Butter_Crab"
    name_ch = "黄油蟹蟹"
    cost_num = 2
    cost_type = CostType.BLACK

    def __init__(self) -> None:
        super().__init__()
        self.food_entity = Butter_Crab_Entity

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

