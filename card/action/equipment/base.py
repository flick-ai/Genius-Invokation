from genius_invocation.card.action.base import ActionCard
from typing import TYPE_CHECKING
from genius_invocation.entity.entity import Entity
from genius_invocation.utils import *

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.zone import CharacterZone
    from genius_invocation.game.player import GeniusPlayer
    from genius_invocation.entity.status import Status, Equipment
class EquipmentCard(ActionCard):
    # 装备牌基本类
    equipment_entity: 'Equipment'
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        pass