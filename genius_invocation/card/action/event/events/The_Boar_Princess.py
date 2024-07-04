from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Combat_Status
from genius_invocation.utils import *

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class The_Boar_Princess_Entity(Combat_Status):
    name: str = 'The Boar Princess'
    name_ch = '野猪公主'
    max_usage = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def update(self, game: 'GeniusGame'):
        self.usage = self.max_usage

    def on_remove(self, game:'GeniusGame'):
        if game.current_remove_from.from_player.index == self.from_player.index:
            dice = self.from_player.roll_dice(game, 1)
            self.from_player.dice_zone.add(dice)
            self.usage -= 1
            if self.usage == 0:
                self.on_destroy(game)

    def on_end(self, game: 'GeniusGame'):
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_EQUIP_REMOVE,ZoneType.ACTIVE_ZONE, self.on_remove),
            (EventType.FINAL_END, ZoneType.ACTIVE_ZONE, self.on_end),
        ]

class The_Boar_Princess(ActionCard):
    id: int = 332025
    name: str = 'The Boar Princess'
    name_ch = '野猪公主'
    time = 4.3
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        entity = game.active_player.team_combat_status.has_status(The_Boar_Princess_Entity)
        if entity != None:
            entity.update(game)
        else:
            game.active_player.team_combat_status.add_entity(
                The_Boar_Princess_Entity(game, game.active_player)
            )

    def find_target(self, game: 'GeniusGame'):
        return [1]
