from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Blessing(ActionCard):
    id: int = 332011
    name: str = "Blessing of the Divine Relic's Installation"
    name_ch = "神宝迁宫祝词"
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()
        self.now_phase: GamePhase = None
        self.artifact = None
        self.artifact_from = None


    def on_played(self, game: 'GeniusGame'):
        target = game.current_action.target_idx
        self.artifact = game.active_player.character_list[target].character_zone.artifact_card
        self.artifact_from = target
        game.active_player.character_list[target].character_zone.artifact_card = None

        self.now_phase = game.game_phase
        game.game_phase = GamePhase.SET_CHARACTER
        game.special_phase = self

    def on_finished(self, game: 'GeniusGame'):
        target = game.current_action.target_idx
        game.active_player.character_list[target].character_zone.artifact_card = self.artifact
        self.artifact.change(game, game.active_player.character_list[target])

        game.game_phase = self.now_phase
        game.special_phase = None

    def find_target(self, game:'GeniusGame'):
        target = []
        for idx, character in game.active_player.character_list:
            if character.character_zone.artifact_card != None:
                has_same = False
                for i, other_character in game.active_player.character_list:
                    if idx == i:
                        continue
                    if other_character.character_zoneartifact_card == None:
                        has_same = True
                        continue
                if has_same:
                    target.append(idx)
        return target

    def refind_target(self, game:'GeniusGame'):
        target = []
        for idx, character in game.active_player.character_list:
            if character.character_zone.artifact_card == None and idx != self.artifact_from:
                target.append(idx+2)
        return target



