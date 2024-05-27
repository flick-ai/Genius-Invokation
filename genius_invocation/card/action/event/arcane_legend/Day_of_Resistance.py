from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Day_of_Resistance_Entity(Status):
    id: int = 330006
    name = "Day of Resistance: Moment of Shattered Dreams"
    name_ch = "抗争之日·碎梦之时"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 4
                
    def on_end(self, game:'GeniusGame'):
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
            (EventType.END_PHASE, ZoneType.ACTIVE_ZONE, self.on_end),
        ]



class Day_of_Resistance(ActionCard):
    id: int = 330006
    name = "Day of Resistance: Moment of Shattered Dreams"
    name_ch = "抗争之日·碎梦之时"
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT_ARCANE_LEGEND
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        game.active_player.team_combat_status.add_entity(Day_of_Resistance_Entity(
            game,
            from_player=game.active_player,
            from_character=get_my_active_character(game),
        ))
    
    def find_target(self, game: 'GeniusGame'):
        if game.active_player.play_arcane_legend:
            return []
        return [1]
