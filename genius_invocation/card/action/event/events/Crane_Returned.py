from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Combat_Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Crane_Returned_Entity(Combat_Status):
    id: int = 332007
    name: str = 'When the Crane Returned'
    name_ch = '鹤归之时'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
    
    def on_after_skill(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_skill.from_character == self.from_character:
                self.from_player.change_to_next_character()
                self.on_destroy(game)
        
    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.on_after_skill),
        ]

class Crane_Returned(ActionCard):
    id: int = 332007
    name: str = 'When the Crane Returned'
    name_ch = '鹤归之时'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        zone = game.active_player.team_combat_status
        if not zone.has_status(Crane_Returned_Entity):
            zone.add_entity(Crane_Returned_Entity(game, game.active_player, None))
