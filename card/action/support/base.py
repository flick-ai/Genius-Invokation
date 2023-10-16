from utils import *
from ..base import ActionCard
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import GeniusGame



class SupportCard(ActionCard):
    # 支援牌基本类
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        idx = game.current_action.target_idx
        game.active_player.support_zone.add_entity(entity=self.entity, idx=idx)
