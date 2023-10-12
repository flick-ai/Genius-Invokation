from typing import TYPE_CHECKING, List
from utils import *
from entity.entity import Entity

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.action import Action
    from game.player import GeniusPlayer
    from event.events import ListenerNode
    from card.character import CharacterSkill

class Character(Entity):
    # 角色基本类
    id: int
    name: str
    element: ElementType
    weapon_type: WeaponType
    country: CountryType
    health_point: int
    max_health_point: int

    '''
        characacter_skill_list包含的是CharacterSkill类, 初始化时会创建skills, 包含的是CharacterSkill类的实例

        后续调用时请调用skills中的实例
    '''
    characacter_skill_list: List[CharacterSkill]
    power: int
    max_power: int

    init_state: list() # 初始状态

    def init_skill(self):
        self.skills = []
        for skill in self.characacter_skill_list:
            self.skills.append(skill(self))

    def __init__(self, game: GeniusGame, from_player: GeniusPlayer, from_character = None):
        super().__init__(game, from_character, from_player)
        self.init_skill()
        self.talent: bool








    # def on_game_start(self):
    #     '''
    #         角色区初始化
    #         讨债人被动 潜行
    #         雷电将军被动 诸愿百眼之轮
    #         无相雷、丘丘等上限修改
    #     '''
    #     return self.power, self.health_point, self.init_state
        

    # def on_round_start(self, game: GeniusGame):
    #     '''
    #         预留
    #     '''
    #     pass

    # def on_switched(self, game: GeniusGame):
    #     '''
    #         passive skill 被动技能 神里绫华
            
    #     '''
    #     pass
