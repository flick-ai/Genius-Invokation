from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


# artifacts
class AdventurerBandana(ArtifactCard):
    '''冒险家头巾'''
    id: int = 0
    name: str = "Adventurer's Bandana"
    cost_num: int = 1
    cost_type: CostType = CostType.WHITE
    max_usage: int = 3

    def __init__(self) -> None:
        super().__init__()
        # self.usages = defaultdict(int)
    
    