from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Status, Frozen_Status
from genius_invocation.card.character.characters.Zhongli import Petrification
from genius_invocation.card.character.characters.HydroHilichurlRogue import MistBubblePrison
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class EdictofAbsolutionEntity(Status):
    id: int = 33000931
    name = "Edict of Absolution"
    name_ch = "赦免宣告"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.from_character.character_zone.immune_list = [Frozen_Status, MistBubblePrison, Petrification]

    def on_change_character(self, game:'GeniusGame'):
        if game.current_switch.from_character == self.from_character:
            if game.current_switch.type == SwitchType.SPECIAL_SWICH:
                game.current_switch = None

    def on_final_end(self, game:'GeniusGame'):
        self.from_character.character_zone.immune_list = None
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_change_character),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE_ZONE, self.on_final_end),
        ]


class EdictofAbsolution(ActionCard):
    id: int = 330009
    name = "Edict of Absolution"
    name_ch = "赦免宣告"
    time = 5.0
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT_ARCANE_LEGEND
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        idx = game.current_action.target_idx
        target = game.active_player.character_list[idx]
        target.character_zone.add_entity(EdictofAbsolutionEntity(
            game,
            from_player=game.active_player,
            from_character=target
        ))

    def find_target(self, game: 'GeniusGame'):
        if game.active_player.play_arcane_legend:
            return []
        target = []
        for character in game.active_player.character_list:
            if character.is_alive:
                target.append(character.index)
        return target
