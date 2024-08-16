from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Status
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class FourLeaf_Sigil(Status):
    name: str = 'Four-Leaf Sigil'
    name_ch = '四叶印'
    id = 33202721
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_end(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if not game.from_character.is_active:
                self.from_player.change_to_id(self.from_character.index)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.ACTIVE_ZONE, self.on_end),
        ]


class FourLeaf(ActionCard):
    id: int = 332027
    name: str = 'Flickering Four-Leaf Sigil'
    name_ch = '浮烁的四叶印'
    time = 4.3
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        target = game.current_action.target_idx
        game.active_player.character_list[target].character_zone.add_entity(
            FourLeaf_Sigil(game, game.active_player, game.active_player.character_list[target])
        )

    def find_target(self, game: 'GeniusGame'):
        target = []
        for idx, character in enumerate(game.active_player.character_list):
            target.append(idx+2)
        return target
