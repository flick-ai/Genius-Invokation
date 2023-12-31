from genius_invocation.entity.entity import Entity
from genius_invocation.utils import *
from typing import TYPE_CHECKING, List, Tuple
from genius_invocation.card.action.equipment.talent.base import TalentCard
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer
    from genius_invocation.game.zone import CharacterZone
from loguru import logger