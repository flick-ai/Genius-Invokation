from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Combat_Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class LoseMoneyEntity(Combat_Status):
    id = 33203631
    name: str = "I'd Rather Lose Money Myself..."
    name_ch = '「看到那小子挣钱…」'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def on_get_dice(self, game:'GeniusGame'):
        if game.current_player.index == 1 - self.from_player.index:
            self.current_usage += 1
            if self.current_usage == 2:
                self.from_player.dice_zone.add([DiceType.OMNI.value])

    def on_end(self, game:'GeniusGame'):
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_GET_DICE, ZoneType.ACTIVE_ZONE, self.on_get_dice),
            (EventType.FINAL_END, ZoneType.ACTIVE_ZONE, self.on_end)
        ]

class LoseMoney(ActionCard):
    id: int = 332036
    name: str = "I'd Rather Lose Money Myself..."
    name_ch = '「看到那小子挣钱…」'
    time = 4.8
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        zone = game.active_player.team_combat_status
        if not zone.has_status(LoseMoneyEntity):
            zone.add_entity(LoseMoneyEntity(game, game.active_player, None))

    def find_target(self, game:'GeniusGame'):
        return [1]