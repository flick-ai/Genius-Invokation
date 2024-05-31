from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Master_of_Weaponry(ActionCard):
    id: int = 332010
    name: str = 'Master of Weaponry'
    name_ch = '诸武精通'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()
        self.now_phase: GamePhase = None
        self.weapon = None
        self.weapon_from = None


    def on_played(self, game: 'GeniusGame'):
        target = game.current_action.target_idx
        self.weapon = game.active_player.character_list[target].character_zone.weapon_card
        self.weapon_from = target
        game.active_player.character_list[target].character_zone.weapon_card = None

        self.now_phase = game.game_phase
        game.game_phase = GamePhase.SET_CHARACTER
        game.special_phase = self

    def on_finished(self, game: 'GeniusGame'):
        target = game.current_action.target_idx
        game.active_player.character_list[target].character_zone.weapon_card = self.weapon
        self.weapon.change(game, game.active_player.character_list[target])

        game.game_phase = self.now_phase
        game.special_phase = None

    def find_target(self, game:'GeniusGame'):
        target = []
        for idx, character in game.active_player.character_list:
            if character.character_zone.weapon_card != None:
                has_same = False
                for i, other_character in game.active_player.character_list:
                    if idx == i:
                        continue
                    if other_character.weapon_type == character.weapon_type and other_character.character_zone.weapon_card == None:
                        has_same = True
                        continue
                if has_same:
                    target.append(idx)
        return target

    def refind_target(self, game:'GeniusGame'):
        target = []
        for idx, character in game.active_player.character_list:
            if character.character_zone.weapon_card == None and character.weapon_type == self.artifact.weapon_card.weapon_type and idx != self.artifact_from:
                target.append(idx+2)
        return target


