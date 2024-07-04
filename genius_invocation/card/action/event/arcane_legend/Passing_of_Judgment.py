from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Combat_Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Passing_of_Judgment_Entity(Combat_Status):
    id: int = 330005
    name = "Passing of Judgment"
    name_ch = "裁定之时"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 3

    def on_play(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_card.card_type in [ActionCardType.EVENT,
                                  ActionCardType.EVENT_ARCANE_LEGEND,
                                  ActionCardType.EVENT_COUNTRY,
                                  ActionCardType.EVENT_ELEMENTAL_RESONANCE,
                                  ActionCardType.EVENT_FOOD]:
                self.usage -= 1
                game.can_play_card = False
                
    def on_end(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
           self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_PLAY_CARD, ZoneType.ACTIVE_ZONE, self.on_play),
            (EventType.END_PHASE, ZoneType.ACTIVE_ZONE, self.on_end),
        ]


class Passing_of_Judgment(ActionCard):
    id: int = 330005
    name = "Passing of Judgment"
    name_ch = "裁定之时"
    time = 4.3
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT_ARCANE_LEGEND
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        game.active_player.team_combat_status.add_entity(Passing_of_Judgment_Entity(
            game,
            from_player=get_opponent(game),
            from_character=None
        ))
    
    def find_target(self, game: 'GeniusGame'):
        if game.active_player.play_arcane_legend:
            return []
        return [1]
