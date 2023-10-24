from genius_invocation.utils import *
from genius_invocation.card.action.base import ActionCard
from typing import TYPE_CHECKING
from loguru import logger

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame



class SupportCard(ActionCard):
    # 支援牌基本类
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:

        idx = game.current_action.target_idx
        game.active_player.support_zone.add_entity(entity=self.entity, idx=idx)
        # logger.info(f"Put {self.name} into {game.active_player.index} Support Zone")

    def find_target(self, game: 'GeniusGame'):
        num = game.active_player.support_zone.num()
        if num != MAX_SUPPORT:
            return [9+num]
        else:
            return [9, 10, 11, 12]

