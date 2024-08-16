from genius_invocation.card.character.base import NormalAttack, ElementalSkill, ElementalBurst, CharacterSkill
from genius_invocation.entity.entity import Entity
from genius_invocation.utils import *
from typing import TYPE_CHECKING, List, Tuple
from genius_invocation.event.damage import Damage
from genius_invocation.event.heal import Heal, BondofLife
from genius_invocation.entity.character import Character
from genius_invocation.entity.status import Status, Combat_Status, Shield, Combat_Shield
from genius_invocation.entity.summon import Summon
from loguru import logger

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer
    from genius_invocation.game.zone import CharacterZone
