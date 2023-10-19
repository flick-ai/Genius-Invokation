from typing import TYPE_CHECKING
from utils import *
from event.Elemental_Reaction import *

if TYPE_CHECKING:
    from game.game import GeniusGame
from loguru import logger

class Damage:
    # 伤害基本类
    def __init__(self, damage_type: 'SkillType', main_damage_element: 'ElementType',
                 main_damage: int, piercing_damage: int,
                 damage_from: 'Entity', damage_to: 'Character',
                 is_plunging_attack: bool=False, is_charged_attack: bool=False) -> None:
        self.damage_type: SkillType = damage_type
        self.main_damage_element: ElementType = main_damage_element
        self.main_damage: int = main_damage
        self.piercing_damage: int = piercing_damage

        self.damage_from: Entity = damage_from
        self.damage_to: Character = damage_to

        self.is_plunging_attack: bool = is_plunging_attack
        self.is_charged_attack: bool = is_charged_attack
        self.reaction: ElementalReactionType = None
        self.swirl_crystallize_type: ElementType = None
        # self.target_idx_bias: int = 0  # The target index is active_idx + target_idx_bias, which therefore, can be defaultly 0.


    @classmethod
    def create_damage(cls, game: 'GeniusGame',
                      damage_type: 'SkillType', main_damage_element: 'ElementType',
                      main_damage: int, piercing_damage: int,
                      damage_from: 'Entity', damage_to: 'Entity',
                      is_plunging_attack: bool=False, is_charged_attack: bool=False):
        dmg = cls(damage_type, main_damage_element, main_damage, piercing_damage, damage_from, damage_to, is_plunging_attack, is_charged_attack)
        return dmg

    # @staticmethod
    # def resolve_damage(game: 'GeniusGame',
    #                 damage_type: 'SkillType', main_damage_element: 'ElementType',
    #                 main_damage: int, piercing_damage: int,
    #                 damage_from: 'Entity', damage_to: 'Entity',
    #                 is_plunging_attack: bool=False, is_charged_attack: bool=False):
    #     dmg = Damage.create_damage(game, damage_type, main_damage_element,
    #                          main_damage, piercing_damage,
    #                          damage_from, damage_to,
    #                          is_plunging_attack, is_charged_attack)
    #     game.damage_list.append(dmg)
        # game.current_damage.elemental_infusion(game)
        # game.current_damage.cal_damage(game)
        # game.current_damage.execute_damage(game)
        # game.current_damage.after_damage(game)

    def on_damage(self, game: 'GeniusGame'):
        self.elemental_infusion(game)
        self.elemental_reaction(game)
        self.damage_add(game)
        self.damage_dealing(game)
        self.damage_excute(game)
        game.suffer_current_damage()
        self.after_damage(game)


    def elemental_infusion(self, game: 'GeniusGame'):
        game.manager.invoke(EventType.INFUSION, game)
    def damage_add(self, game: 'GeniusGame'):
        logger.debug(f"Before Damage Add: {game.current_damage.main_damage}")
        # import ipdb; ipdb.set_trace()
        game.manager.invoke(EventType.DAMAGE_ADD, game)
        logger.debug(f"After Damage Add: {game.current_damage.main_damage}")

    def damage_dealing(self, game: 'GeniusGame'):
        game.manager.invoke(EventType.DEALING_DAMAGE, game)

    def damage_excute(self, game: 'GeniusGame'):
        logger.debug(f"Before Damage Excute: {game.current_damage.main_damage}")
        game.manager.invoke(EventType.EXCUTE_DAMAGE, game)
        logger.debug(f"After Damage Excute: {game.current_damage.main_damage}")


    def after_damage(self, game: 'GeniusGame'):
        game.manager.invoke(EventType.AFTER_TAKES_DMG, game)
        pass

    # def cal_damage(self, game: 'GeniusGame'): NO USE
    #     # 元素类型转化 On_Infusion
    #     '''
    #     Based on my activeZone.
    #     '''
    #     # 元素反应
    #     '''
    #     Based on elemental Reation.
    #     '''
    #     self.elemental_reaction(game)
    #     # 可能产生新的独立伤害（扩散), 这一部分需要在当前伤害结算完毕后再进行

    #     # 伤害加算
    #     '''
    #     '''
    #     pass

    def elemental_reaction(self, game: 'GeniusGame'):
        '''
        It will update game.current_damage, .
        '''
        damage = game.current_damage
        targetplayer_id = 1 - game.active_player_index
        targetplayer = game.players[targetplayer_id]
        target_character = damage.damage_to
        logger.info(target_character.name)
        logger.info(target_character.elemental_application)
        target_index = target_character.index
        Reaction = None
        Swirl_Crystallize_type = None

        # No attachment on Target
        if len(target_character.elemental_application) == 0:
            match damage.main_damage_element:
                case ElementType.CRYO | ElementType.HYDRO | ElementType.PYRO | ElementType.ELECTRO:
                    target_character.elemental_application.insert(0, damage.main_damage_element)
                case ElementType.DENDRO:
                    target_character.elemental_application.append(damage.main_damage_element)
            self.reaction = None
            self.swirl_crystallize_type = None
            return


        targetAttachElement = target_character.elemental_application[0]

        match damage.main_damage_element:
            case ElementType.CRYO: # 冰
                match targetAttachElement:
                    case ElementType.HYDRO: # 水
                        game.current_damage.main_damage += 1
                        Frozen(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Frozen
                    case ElementType.PYRO: # 火
                        game.current_damage.main_damage += 2
                        Melt(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Melt
                    case ElementType.ELECTRO:
                        game.current_damage.main_damage += 1
                        game.current_damage.piercing_damage += 1
                        Superconduct(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Superconduct
            case ElementType.HYDRO: # 水
                match targetAttachElement:
                    case ElementType.CRYO:
                        game.current_damage.main_damage += 1
                        Frozen(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Frozen
                    case ElementType.PYRO:
                        game.current_damage.main_damage += 2
                        Vaporize(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Vaporize
                    case ElementType.ELECTRO:
                        game.current_damage.main_damage += 1
                        game.current_damage.piercing_damage += 1
                        Electro_Charged(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Electro_Charged
                    case ElementType.DENDRO:
                        game.current_damage.main_damage += 1
                        Bloom(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Bloom
            case ElementType.PYRO: # 火
                match targetAttachElement:
                    case ElementType.CRYO:
                        game.current_damage.main_damage += 2
                        Melt(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Frozen
                    case ElementType.HYDRO:
                        game.current_damage.main_damage += 2
                        Vaporize(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Vaporize
                    case ElementType.ELECTRO:
                        game.current_damage.main_damage += 2
                        Overloaded(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Overloaded
                    case ElementType.DENDRO:
                        game.current_damage.main_damage += 1
                        Burning(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Burning

            case ElementType.ELECTRO: # 雷
                match targetAttachElement:
                    case ElementType.CRYO:
                        game.current_damage.main_damage += 1
                        game.current_damage.piercing_damage += 1
                        Superconduct(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Superconduct
                    case ElementType.HYDRO:
                        game.current_damage.main_damage += 1
                        game.current_damage.piercing_damage += 1
                        Electro_Charged(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Electro_Charged
                    case ElementType.PYRO:
                        game.current_damage.main_damage += 2
                        Overloaded(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Overloaded
                    case ElementType.DENDRO:
                        game.current_damage.main_damage += 1
                        Quicken(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Quicken

            case ElementType.DENDRO: # 草
                match targetAttachElement:
                    case ElementType.HYDRO:
                        game.current_damage.main_damage += 1
                        Bloom(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Bloom
                    case ElementType.PYRO:
                        game.current_damage.main_damage += 1
                        Burning(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Burning
                    case ElementType.ELECTRO:
                        game.current_damage.main_damage += 1
                        Quicken(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Quicken

            case ElementType.ANEPMO: # 风
                match targetAttachElement:
                    case ElementType.CRYO | ElementType.HYDRO | ElementType.PYRO | ElementType.ELECTRO:
                        Swirl(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Swirl
                        Swirl_Crystallize_type = targetAttachElement

            case ElementType.GEO: # 岩
                match targetAttachElement:
                    case ElementType.CRYO | ElementType.HYDRO | ElementType.PYRO | ElementType.ELECTRO:
                        game.current_damage.main_damage += 1
                        Crystallize(game, targetplayer_id, target_index)
                        Reaction = ElementalReactionType.Crystallize
                        Swirl_Crystallize_type = targetAttachElement
        if Reaction is None:
            match damage.main_damage_element:
                case ElementType.CRYO | ElementType.HYDRO | ElementType.PYRO | ElementType.ELECTRO:
                    if not damage.main_damage_element in target_character.elemental_application:
                        target_character.elemental_application.insert(0, damage.main_damage_element)
                case ElementType.DENDRO:
                    if not damage.main_damage_element in target_character.elemental_application:
                        target_character.elemental_application.append(damage.main_damage_element)

        self.reaction = Reaction
        self.swirl_crystallize_type = Swirl_Crystallize_type

        if self.reaction == ElementalReactionType.Swirl:
            targetlist = []
            for id in range(targetplayer.character_num):
                targetlist.append((id + targetplayer.active_idx)%targetplayer.character_num)

            targetlist.remove(target_index)
            for id in targetlist:
                if targetplayer.character_list[id].is_alive:
                    dmg = Damage.create_damage(
                        game,
                        SkillType.OTHER,
                        Swirl_Crystallize_type,
                        1,
                        0,
                        self.damage_from,
                        targetplayer.character_list[id],
                    )
                    game.add_damage(dmg)