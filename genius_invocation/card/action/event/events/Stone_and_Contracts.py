from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Combat_Status

from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class  Stone_and_Contracts_Entity(Combat_Status):
    id: int = 331802
    name: str = 'Stone and Contracts'
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
    
    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.from_player.dice_zone.add([7,7,7])
            self.on_destroy(self)
        
    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.ACTIVE_ZONE, self.on_begin),
        ]
    

        
class Stone_and_Contracts(ActionCard):
    id: int = 331802
    name: str = 'Stone and Contracts'
    cost_num = 3
    cost_type = CostType.BLACK
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        game.active_player.team_combat_status.add_entity(Stone_and_Contracts_Entity(
            game,
            from_player=game.active_player,
            from_character=None
        ))