from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Combat_Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Falls_and_Fortune_Entity(Combat_Status):
    name: str = 'Falls and Fortune'
    name_ch = '坍陷与契机'
    id = 33202631
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def on_calculate(self, game:'GeniusGame'):
        if game.current_dice.use_type == 'change character':
            game.current_dice.cost[0]['cost_num'] += 1

    def on_change(self, game:'GeniusGame'):
        self.on_calculate(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.ACTIVE_ZONE, self.on_calculate),
            (EventType.ON_CHANGE_CHARACTER, ZoneType.ACTIVE_ZONE, self.on_change)
        ]

class Falls_and_Fortune(ActionCard):
    id: int = 332026
    name: str = 'Falls and Fortune'
    name_ch = '坍陷与契机'
    time = 4.3
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        zone = game.active_player.team_combat_status
        if not zone.has_status(Falls_and_Fortune_Entity):
            zone.add_entity(Falls_and_Fortune_Entity(game, game.active_player, None))

    def find_target(self, game:'GeniusGame'):
        if game.active_player.dice_zone.num() >= 8 and not get_opponent(game).is_pass:
            return [1]
        else:
            return []

    def balance_adjustment():
        log = {
            4.8:"调整了事件牌「坍陷与契机」所需元素骰：由1个元素骰调整为0个元素骰。",
        }
        return log