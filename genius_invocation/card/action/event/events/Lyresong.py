from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Combat_Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class LyresongStatus(Combat_Status):
    name: str = 'Lyresong'
    name_ch = '琴音之诗'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == ActionCardType.EQUIPMENT_ARTIFACT:
                if game.current_dice.cost[0]['cost_num']>0:
                    game.current_dice.cost[0]['cost_num'] = max(game.current_dice.cost[0]['cost_num']-2, 0)
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

class Lyresong(ActionCard):
    id: int = 332024
    name: str = 'Lyresong'
    name_ch = '琴音之诗'
    time = 4.2
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        target = game.current_action.target_idx
        card = game.active_player.character_list[target].character_zone.artifact_card.artifact_card
        game.active_player.character_list[target].character_zone.artifact_card.on_destroy(game)
        game.active_player.character_list[target].character_zone.artifact_card = None
        game.active_player.hand_zone.add([card])

        zone = game.active_player.team_combat_status
        if not zone.has_status(LyresongStatus):
            zone.add_entity(LyresongStatus(game, game.active_player, None))

    def find_target(self, game:'GeniusGame'):
        target = []
        for idx, character in enumerate(game.active_player.character_list):
            if character.character_zone.artifact_card != None:
                target.append(idx+2)
        return target