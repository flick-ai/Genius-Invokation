from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Combat_Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Dream(Combat_Status):
    name: str = 'Rhythm of the Great Dream'
    name_ch = '大梦的曲调'
    id = 33202131
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
    
    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == ActionCardType.EQUIPMENT_WEAPON or game.current_dice.use_type == ActionCardType.EQUIPMENT_ARTIFACT:
                if game.current_dice.cost[0]['cost_num']>0:
                    game.current_dice.cost[0]['cost_num'] -= 1
                    return True
        return False
    
    def on_play_card(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.on_destroy(game)
        
    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.ACTIVE_ZONE, self.on_calculate),
            (EventType.ON_PLAY_CARD, ZoneType.ACTIVE_ZONE, self.on_play_card),
        ]

class Great_Dream(ActionCard):
    id: int = 332021
    name: str = 'Rhythm of the Great Dream'
    name_ch = '大梦的曲调'
    time = 3.8
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        zone = game.active_player.team_combat_status
        if not zone.has_status(Dream):
            zone.add_entity(Dream(game, game.active_player, None))
