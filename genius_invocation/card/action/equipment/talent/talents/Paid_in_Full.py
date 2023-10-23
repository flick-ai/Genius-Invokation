from utils import *
from typing import TYPE_CHECKING
from genius_invocation.card.action.equipment.talent.base import TalentCard
from genius_invocation.card.character.characters.FatuiPyroAgent import Fatui_Pyro_Agent
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Paid_in_Full(TalentCard):
    name = 'Paid in Full'
    name_ch = "悉数讨回"
    def __init__(self) -> None:
        super().__init__()
        self.character = Fatui_Pyro_Agent
        self.skill_idx = 1