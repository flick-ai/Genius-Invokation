from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Combat_Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Changing_Shifts_Entity(Combat_Status):
    id: int = 332002
    name: str = 'Changing Shifts'
    name_ch = '换班时间'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == SwitchType.CHANGE_CHARACTER:
                if game.current_dice.cost[0]['cost_num'] > 0:
                    game.current_dice.cost[0]['cost_num'] -= 1
                    return True
        return False

    def on_change(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_CHANGE_CHARACTER, ZoneType.ACTIVE_ZONE, self.on_change),
            (EventType.CALCULATE_DICE, ZoneType.ACTIVE_ZONE, self.on_calculate),
        ]

class Changing_Shifts(ActionCard):
    id: int = 332002
    name: str = 'Changing Shifts'
    name_ch = '换班时间'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        zone = game.active_player.team_combat_status
        if not zone.has_status(Changing_Shifts_Entity):
            zone.add_entity(Changing_Shifts_Entity(game, game.active_player, None))
