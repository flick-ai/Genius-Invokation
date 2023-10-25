from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Combat_Status
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Switch_Entity(Combat_Status):
    id: int = 332006
    name = 'Leave it to me!'
    name_ch = '交给我吧'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def on_change(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.from_player.is_quick_change == True
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_CHANGE_CHARACTER, ZoneType.ACTIVE_ZONE, self.on_change),
        ]

class Leave_it_to_Me(ActionCard):
    id: int = 332006
    name: str = 'Leave it to Me!'
    name_ch = '交给我吧'
    cost_num =0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        if not game.active_player.team_combat_status.has_status(Switch_Entity):
            game.active_player.team_combat_status.add_entity(Switch_Entity(game, game.active_player))
        