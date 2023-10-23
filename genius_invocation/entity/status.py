from genius_invocation.entity.entity import Entity
from genius_invocation.utils import *
from typing import TYPE_CHECKING, List, Tuple


if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.action import Action
    from genius_invocation.event.events import ListenerNode
    from genius_invocation.game.player import GeniusPlayer

#TODO: FINISH THE ENTITIES

class Status(Entity):
    # 状态基本类
    id: int
    name: str
    name_ch: str

    def __init__(self, game: 'GeniusGame', from_player:'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage: int #生成时的可用次数
        self.max_usage: int #Maybe changed by Talent.
        self.current_usage: int

    def on_destroy(self, game):
        super().on_destroy(game)
        if self.from_character is not None:
            self.from_character.character_zone.remove_entity(self)

    def update(self):
        # All states can be update, maybe need to re-implement in subclass
        pass

    def show(self):
        try:
            return str(self.current_usage)
        except:
            return "^(._.)<^"

class Combat_Status(Entity):
    id: int
    name: str
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage: int #生成时的可用次数
        self.max_usage: int #Maybe changed by Talent.
        self.current_usage: int

    def on_destroy(self, game):
        super().on_destroy(game)
        self.from_player.team_combat_status.remove_entity(self)

    def show(self):
        try:
            return str(self.current_usage)
        except:
            return "^(._.)<^"

class Shield(Status):
    # Status of shield (Only for single character)
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
    def on_destroy(self, game):
        super().on_destroy(game)

class Combat_Shield(Combat_Status):
    # Combat_Status of shield.
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_destroy(self, game):
        super().on_destroy(game)
class Equipment(Entity):
    pass

class Weapon(Equipment):
    # 武器实体
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: "Character"= None, weapon_card: 'Weapon' = None):
        super().__init__(game, from_player, from_character)
        self.weapon_card = weapon_card

    def on_destroy(self, game):
        super().on_destroy(game)
        self.from_character.character_zone.weapon_card = None

    def get_weapon_card(self, game: 'GeniusGame'):
        self.on_destroy(game)
        return self.weapon_card
    def show(self):
        return self.name
class Artifact(Equipment):
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: "Character"= None, artifact_card: 'Artifact' = None):
        super().__init__(game, from_player, from_character)
        self.artifact_card = artifact_card

    def on_destroy(self, game):
        super().on_destroy(game)
        self.from_character.character_zone.weapon_card = None

    def get_artifact_card(self, game: 'GeniusGame'):
        self.on_destroy(game)
        return self.artifact_card

    def show(self):
        return self.name

# TODO: Maybe need to move to other places in future
class Frozen_Status(Status):
    name = 'Frozen'
    name_ch = "冻结"
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
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin_phase),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage)
        ]


class Dendro_Core(Combat_Status):
    name = 'Dendro Core'
    name_ch = "草原核"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1
        self.max_usage = 1

    def update(self):
        self.current_usage = self.usage

    def add_one_usage(self):
        self.current_usage = self.current_usage+1

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
    id = 12345
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

    def on_excuete_dmg(self,game: 'GeniusGame'):
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
            (EventType.EXECUTE_DAMAGE, ZoneType.ACTIVE_ZONE_SHIELD, self.on_excuete_dmg)
        ]

class Satisfy_Statue(Status):
    name = "Satisfy"
    name_ch = "饱腹"
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




