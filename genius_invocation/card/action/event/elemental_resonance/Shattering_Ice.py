from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Status
from genius_invocation.utils import *

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Shattering_Ice_Entity(Status):
    id: int = 331102
    name: str = "Shattering_Ice"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
    
    def on_damage_add(self, game: 'GeniusGame'):
        print(game.current_damage.damage_from.name, self.from_character.name)
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PIERCING:
                return
            else:
                game.current_damage.main_damage += 2
                self.current_usage -=1
                if self.current_usage <=0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
        ]

class Shattering_Ice(ActionCard):
    id: int = 331102
    name: str = "Shattering_Ice"
    cost_num = 1
    card_type = ActionCardType.EVENT_ELEMENTAL_RESONANCE.value
    cost_type = CostType.CRYO

    def __init__(self) -> None:
        super().__init__()
        self.elemental_resonance_entity = Shattering_Ice_Entity

    def on_played(self, game: 'GeniusGame') -> None:
        target_character = get_active_character(game, game.active_player.index)
        target_character.character_zone.add_entity(self.elemental_resonance_entity(game, from_player=game.active_player, from_character=target_character))