from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Combat_Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Pankration_Entity(Combat_Status):
    name: str = 'Pankration!'
    name_ch = '拳力斗技！'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
    
    def on_after_any(self, game:'GeniusGame'):
        if game.active_player.is_pass and not get_opponent(game).is_pass:
            self.from_player.get_card(num=2)
        
    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_ANY_ACTION, ZoneType.ACTIVE_ZONE, self.on_after_any),
        ]

class Pankration(ActionCard):
    id: int = 332022
    name: str = 'Pankration!'
    name_ch = '拳力斗技！'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        zone = game.active_player.team_combat_status
        if not zone.has_status(Pankration_Entity):
            zone.add_entity(Pankration_Entity(game, game.active_player, None))
    
    def find_target(self, game:'GeniusGame'):
        if game.active_player.dice_zone.num() >= 8 and not get_opponent(game).is_pass:
            return [1]
        else:
            return []