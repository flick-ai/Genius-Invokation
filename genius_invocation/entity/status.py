from genius_invocation.entity.entity import Entity
from genius_invocation.utils import *
from typing import TYPE_CHECKING, List, Tuple


if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.action import Action
    from genius_invocation.event.events import ListenerNode
    from genius_invocation.game.player import GeniusPlayer
    from genius_invocation.card.action.equipment.weapon.base import WeaponCard
    from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
    from genius_invocation.card.action.equipment.specialskill.base import SpecialSkillCard

#TODO: FINISH THE ENTITIES

class Status(Entity):
    # 状态基本类
    id: int
    name: str
    name_ch: str

    def __init__(self, game: 'GeniusGame', from_player:'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage: int #生成时的可用次数
        # self.max_usage: int #Maybe No Use except some special status. Please add it in subclass.
        self.current_usage: int

    def on_destroy(self, game):
        super().on_destroy(game)
        if self.from_character is not None:
            self.from_character.character_zone.remove_entity(self)

    def update(self):
        # All states can be update, maybe need to re-implement in subclass
        self.current_usage = max(self.current_usage, self.usage)

    def show(self):
        try:
            return str(self.current_usage)
        except:
            return "^(._.)^"

class Combat_Status(Entity):
    id: int
    name: str
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage: int #生成时的可用次数
        # self.max_usage: int #Maybe No Use except some special status. Please add it in subclass.
        self.current_usage: int
    def update(self):
        # All states can be update, maybe need to re-implement in subclass
        self.current_usage = max(self.current_usage, self.usage)
    def on_destroy(self, game):
        super().on_destroy(game)
        self.from_player.team_combat_status.remove_entity(self)

    def show(self):
        try:
            return str(self.current_usage)
        except:
            return "^(._.)^"

class Shield(Status):
    # Status of shield (Only for single character)
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None, usage=1):
        super().__init__(game, from_player, from_character)
        self.current_usage = usage

    def on_destroy(self, game):
        super().on_destroy(game)

    def on_execute_dmg(self,game: 'GeniusGame'):
        if game.current_damage.main_damage_element != ElementType.PIERCING:
            if game.current_damage.damage_to == self.from_character:
                if game.current_damage.main_damage >= self.current_usage:
                    game.current_damage.main_damage -= self.current_usage
                    self.current_usage = 0
                    self.on_destroy(game)
                else:
                    self.current_usage -= game.current_damage.main_damage
                    game.current_damage.main_damage = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_execute_dmg)
        ]

class Combat_Shield(Combat_Status):
    # Combat_Status of shield.
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_destroy(self, game):
        super().on_destroy(game)

    def on_execute_dmg(self,game: 'GeniusGame'):
        if game.current_damage.main_damage_element != ElementType.PIERCING:
            if game.current_damage.damage_to.from_player == self.from_player:
                if game.current_damage.damage_to.is_active:
                    if game.current_damage.main_damage >= self.current_usage:
                        game.current_damage.main_damage -= self.current_usage
                        self.current_usage = 0
                        self.on_destroy(game)
                    else:
                        self.current_usage -= game.current_damage.main_damage
                        game.current_damage.main_damage = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.ACTIVE_ZONE_SHIELD, self.on_execute_dmg)
        ]


class Equipment(Entity):
    def on_destroy(self, game):
        super().on_destroy(game)
        game.current_remove_from = self.from_character
        game.manager.invoke(EventType.ON_EQUIP_REMOVE, game)
        game.current_remove_from = None

class Weapon(Equipment):
    # 武器实体
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: "Character"= None, weapon_card: 'WeaponCard' = None):
        super().__init__(game, from_player, from_character)
        self.weapon_card = weapon_card

    def on_destroy(self, game):
        super().on_destroy(game)
        self.from_character.character_zone.weapon_card = None

    def get_weapon_card(self, game: 'GeniusGame'):
        '''Get the weapon card from the character to hands.'''
        self.on_destroy(game)
        return self.weapon_card

    def change(self, game, target):
        self.from_character = target

    def show(self):
        return self.name_ch

    def count_cost(self):
        return self.weapon_card.cost_num


class Artifact(Equipment):
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: "Character"= None, artifact_card: 'ArtifactCard' = None):
        super().__init__(game, from_player, from_character)
        self.artifact_card = artifact_card

    def on_destroy(self, game):
        super().on_destroy(game)
        self.from_character.character_zone.artifact_card = None

    def get_artifact_card(self, game: 'GeniusGame'):
        '''Get the artifact card from the character to hands.'''
        self.on_destroy(game)
        return self.artifact_card

    def show(self):
        return self.name_ch

    def count_cost(self):
        return self.artifact_card.cost_num

class SpecialSkill(Equipment):
    type = SkillType.SPECIAL_SKILL
    cost = [{'cost_num': 0, 'cost_type': CostType.BLACK}]
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: "Character"= None, card: 'SpecialSkillCard' = None):
        super().__init__(game, from_player, from_character)
        self.skill_card = card
        self.usage = 0

    def check_usage(self, game):
        self.usage -= 1
        if self.usage <= 0:
            self.on_destroy(game)

    def update(self, usage=1):
        self.usage += usage

    def on_destroy(self, game):
        super().on_destroy(game)
        self.from_character.character_zone.special_skill = None

    def on_call(self, game):
        game.manager.invoke(EventType.ON_USE_SPECIAL, game)

    def find_target(self, game: 'GeniusGame'):
        return [0]

    def show(self):
        return self.name_ch

    def count_cost(self):
        return self.skill_card.cost_num


# TODO: Maybe need to move to other places in future
class Frozen_Status(Status):
    name = 'Frozen'
    name_ch = "冻结"
    id = 22
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.max_usage = 1
        self.current_usage = 1
        self.from_character.is_frozen = True

    def update(self):
        self.current_usage = self.usage

    def on_destroy(self, game):
        super().on_destroy(game)
        self.from_character.is_frozen = False

    def on_begin_phase(self, game: 'GeniusGame'):
        self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)

    def on_add_damage(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL or game.current_damage.main_damage_element == ElementType.PYRO:
                game.current_damage.main_damage += 2
                self.current_usage -= 1
                if self.current_usage <= 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_begin_phase),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage)
        ]


class Dendro_Core(Combat_Status):
    name = 'Dendro Core'
    name_ch = "草原核"
    id = 31
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1
        self.max_usage = 1

    def update(self):
        self.current_usage = self.usage

    def add_one_usage(self):
        self.current_usage = self.current_usage+1

    def lose_one_usage(self, game):
        self.current_usage = self.current_usage-1
        if self.current_usage <= 0:
            self.on_destroy(game)

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from is None: return
        if game.current_damage.damage_from.from_player == self.from_player:
            if game.current_damage.main_damage_element == ElementType.PYRO or game.current_damage.main_damage_element == ElementType.ELECTRO:
                game.current_damage.main_damage += 2
                self.current_usage -= 1
                if self.current_usage <= 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.on_damage_add)
        ]

class Catalyzing_Feild(Combat_Status):
    name = 'Catalyzing Feild'
    name_ch = "激化领域"
    id = 32
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2
        self.max_usage = 4

    def update(self):
        self.current_usage = self.usage

    def add_one_usage(self):
        self.current_usage = self.current_usage+1

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from is None: return
        if game.current_damage.damage_from.from_player == self.from_player:
            if game.current_damage.main_damage_element == ElementType.DENDRO or game.current_damage.main_damage_element == ElementType.ELECTRO:
                game.current_damage.main_damage += 1
                self.current_usage -= 1
                if self.current_usage <= 0:
                    self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.on_damage_add)
        ]
class Crystallize_Shield(Combat_Shield):
    id = 51
    name = "Crystallize Shield"
    name_ch = "结晶盾"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1
        self.max_usage = 2

    def update(self):
        if self.current_usage < self.max_usage:
            self.current_usage += 1

class Satisfy_Statue(Status):
    name = "Satisfy"
    name_ch = "饱腹"
    id = 21
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
        self.from_character.is_satisfy = True

    def update(self):
        self.current_usage = self.usage
    def show(self):
        return str("╮(╯▽╰)╭")
    def on_destroy(self, game):
        super().on_destroy(game)
        self.from_character.is_satisfy = False

    def on_begin_phase(self, game: 'GeniusGame'):
        self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin_phase),
        ]

class GoldenChalice(Combat_Status):
    name = "Golden Chalice's Bounty"
    name_ch = "金杯的丰馈"
    id = 120831
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = MAX_ROUND
        self.current_usage = self.usage



