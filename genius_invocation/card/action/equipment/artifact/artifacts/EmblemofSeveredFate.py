from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class EmblemofSeveredFateEntity(Artifact):
    name: str = "Emblem of Severed Fate"
    name_ch = "绝缘之旗印"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)

    def update(self):
        pass
    
    def on_add_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.ELEMENTAL_BURST:
                game.current_damage.main_damage += 2

    def on_after_skill(self, game:'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player:
            if game.current_skill.from_character != self.from_character:
                if game.current_skill.type == SkillType.ELEMENTAL_BURST:
                   self.from_character.get_power(power=1)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_after_skill),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage)
        ]



class EmblemofSeveredFate(ArtifactCard):
    id: int = 312008
    name: str = "Emblem of Severed Fate"
    name_ch = "绝缘之旗印"
    time = 3.7
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = EmblemofSeveredFateEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.0] = "调整了装备牌「绝缘之旗印」所需元素骰费用：所需元素骰费用由3个任意元素骰调整为2个元素骰"
        log[4.1] = "调整了装备牌「绝缘之旗印」的效果：现在该牌的效果每回合至多触发1次"
        return log

