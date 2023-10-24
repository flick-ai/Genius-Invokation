from typing import TYPE_CHECKING, List
from genius_invocation.utils import *
from genius_invocation.entity.entity import Entity
from genius_invocation.event.Elemental_Reaction import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.zone import CharacterZone
    from genius_invocation.game.action import Action
    from genius_invocation.game.player import GeniusPlayer
    from genius_invocation.event.events import ListenerNode
    from genius_invocation.card.character import CharacterSkill
    from genius_invocation.entity.status import Status

class Character(Entity):
    # 角色基本类
    id: int #Identity document, 卡牌的编号，可能用来喂给state for RL。
    name: str
    element: ElementType
    weapon_type: WeaponType
    country: CountryType
    init_health_point: int
    # health_point: int
    max_health_point: int

    '''
        characacter_skill_list包含的是CharacterSkill类, 初始化时会创建skills, 包含的是CharacterSkill类的实例

        后续调用时请调用skills中的实例
    '''
    # skill_list: List['CharacterSkill'] 这么写怪怪的
    skill_list: List
    power: int
    max_power: int
    talent_skill: 'CharacterSkill'
    # init_state: list() # 初始状态
    def init_state(self, game: 'GeniusGame'):
        '''
            游戏开始时的被动技能
        '''
        pass

    def init_skill(self):
        self.skills = []
        for skill in self.skill_list:
            self.skills.append(skill(self))
        
    def on_begin(self, game: 'GeniusGame'):
        '''
            回合开始时, 刷新所有技能的使用次数
        '''
        for skill in self.skills:
            skill.usage_this_round = 0

    def on_switched_to(self):
        '''
            被切换到时调用
        '''
        self.from_player.is_after_change = True
    def refresh_talent(self, game:'GeniusGame'):
        pass #Maybe some talent can refresh some state repeatly.
        # Should be implement in subclass.

    def listen_talent_events(self, game:'GeniusGame'):
        pass
        # Should be implement in subclass.
        # Add events that only will be invoked with talent equiped into managers.

    def equip_talent(self, game:'GeniusGame', is_action = True):
        if self.talent:
            self.refresh_talent(game)
            if is_action:
                self.talent_skill.on_call(game)
        else:
            self.talent = True
            self.listen_talent_events(game)
            if is_action:
                self.talent_skill.on_call(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
        ]

    def skill(self, skill, game: 'GeniusGame'):
        self.skills[skill].on_call(game)

    def __init__(self, game: 'GeniusGame', character_zone:'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None):
        self.character_zone = character_zone
        self.init_skill()
        self.talent: bool = False
        self.is_active: bool = False
        self.is_alive: bool = True
        self.is_frozen: bool = False
        self.is_satisfy: bool = False
        self.health_point = self.init_health_point
        self.power: int = 0 # 初始充能
        self.elemental_application: List['ElementType'] = []
        self.index: int = index
        super().__init__(game, from_player, from_character)
        self.init_state(game)

    def heal(self, heal: int):
        if self.is_alive:
            self.health_point += heal
            if self.health_point > self.max_health_point:
                self.health_point = self.max_health_point

    def dying(self, game: 'GeniusGame'):
        assert self.is_alive==False
        self.is_frozen = False
        self.is_active = False
        self.talent = False
        self.power = 0
        self.elemental_attach = None
        self.character_zone.clear(game)

    def revive(self, game: 'GeniusGame'):
        # Basic revive.
        assert self.is_alive == False
        self.is_alive = True
        self.health_point = 1

    def show(self):
        return str(self.health_point)

    def elemental_attach(self, game: 'GeniusGame', element: 'ElementType'):
        assert element in [ElementType.CRYO, ElementType.DENDRO, ElementType.ELECTRO, ElementType.HYDRO, ElementType.PYRO]
        if len(self.elemental_application) == 0:
            self.elemental_application.append(element)
            return
        
        attached = self.elemental_application[0]
        Reaction = None
        targetplayer_id = self.from_player.index
        target_index = self.index # Target is myself.
        match attached:
            case ElementType.CRYO:
                match element:
                    case ElementType.HYDRO:
                        Frozen(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Frozen
                    case ElementType.PYRO: # 火
                        Melt(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Melt
                    case ElementType.ELECTRO: # 雷
                        Superconduct(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Superconduct
            case ElementType.HYDRO:
                match element:
                    case ElementType.CRYO:
                        Frozen(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Frozen
                    case ElementType.PYRO:
                        Vaporize(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Vaporize
                    case ElementType.ELECTRO:
                        Electro_Charged(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Electro_Charged
                    case ElementType.DENDRO:
                        Bloom(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Bloom
            case ElementType.PYRO:
                match element:
                    case ElementType.CRYO:
                        Melt(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Frozen
                    case ElementType.HYDRO:
                        Vaporize(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Vaporize
                    case ElementType.ELECTRO:
                        Overloaded(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Overloaded
                    case ElementType.DENDRO:
                        Burning(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Burning
            case ElementType.ELECTRO:
                match element:
                    case ElementType.CRYO:
                        Superconduct(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Superconduct
                    case ElementType.HYDRO:
                        Electro_Charged(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Electro_Charged
                    case ElementType.PYRO:
                        Overloaded(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Overloaded
                    case ElementType.DENDRO:
                        Quicken(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Quicken
            case ElementType.DENDRO:
                match element:
                    case ElementType.HYDRO:
                        Bloom(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Bloom
                    case ElementType.PYRO:
                        Burning(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Burning
                    case ElementType.ELECTRO:
                        Quicken(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Quicken
        if Reaction is None and (not element in self.elemental_application):
            match element:
                case ElementType.CRYO | ElementType.HYDRO | ElementType.PYRO | ElementType.ELECTRO:
                    self.elemental_application.insert(0, element)
                case ElementType.DENDRO:
                    self.elemental_application.append(element)
        if Reaction is not None:
            game.manager.invoke(EventType.ELEMENTAL_APPLICATION_REATION, game)
        
        if Reaction == ElementalReactionType.Overloaded:
            if self.is_active:
                self.from_player.change_to_next_character()
        return Reaction
