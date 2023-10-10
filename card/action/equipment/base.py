from ..base import ActionCard
from game.game import GeniusGame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.zone import CharacterZone
    from game.player import GeniusPlayer


class EquipmentCard(ActionCard):
    # 装备牌基本类
    character: "CharacterZone"
    player: "GeniusPlayer"

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: GeniusGame) -> None:
        target = game.current_action.target_idx
        self.character = game.players[game.active_player].active_zone.character_list[target]
        self.player = game.players[game.active_player]