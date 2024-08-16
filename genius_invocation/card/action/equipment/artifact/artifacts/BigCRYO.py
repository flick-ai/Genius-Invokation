from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard, SmallElement, BigElement
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class BigCRYO_Entity(BigElement):
    name: str = "Blizzard Strayer"
    name_ch = "冰风迷途的勇士"
    element_type = CostType.CRYO
    id = 31210291
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)


class BigCRYO(ArtifactCard):
    id: int = 312102
    name: str = "Blizzard Strayer"
    name_ch = "冰风迷途的勇士"
    cost_num: int = 1
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = BigCRYO_Entity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[3.6] = "调整了「七圣召唤」中，装备牌「冰风迷途的勇士」「沉沦之心」「炽烈的炎之魔女」「如雷的盛怒」「翠绿之影」「悠古的磐岩」「深林的记忆」所需的元素骰子：所需骰子由3个同元素骰子调整为3个任意元素骰子"
        log[4.0] = "调整了装备牌「冰风迷途的勇士」、「沉沦之心」、「炽烈的炎之魔女」、「如雷的盛怒」、「翠绿之影」、「悠古的磐岩」、「深林的记忆」所需元素骰费用：所需元素骰费用由3个任意元素骰调整为2个相同元素骰"
        return log

