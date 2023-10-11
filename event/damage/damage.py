
from utils import *
from game.game import GeniusGame
from event.Elemental_Reaction import *
class Damage:
    # 伤害基本类
    def __init__(self, damage_type: SkillType, main_damage_element: ElementType, 
                 main_damage: int, piercing_damage: int, 
                 damage_from: Entity, damage_to: Entity,
                 is_plunging_attack: bool=False, is_charged_attack: bool=False) -> None:
        self.damage_type: SkillType = damage_type
        self.main_damage_element: ElementType = main_damage_element
        self.main_damage: int = main_damage
        self.piercing_damage: int = piercing_damage

        self.damage_from: Entity = damage_from
        self.damage_to: Entity = damage_to

        self.is_plunging_attack: bool = is_plunging_attack
        self.is_charged_attack: bool = is_charged_attack
        self.reaction: ElementalReactionType = None
        self.swirl_crystalize_type: ElementType = None
        self.target_idx_bias: int = 0  # The target index is active_idx + target_idx_bias, which therefore, can be defaultly 0.
    

    @classmethod
    def create_damage(cls, game: GeniusGame,
                      damage_type: SkillType, main_damage_element: ElementType, 
                      main_damage: int, piercing_damage: int, 
                      damage_from: Entity, damage_to: Entity,
                      is_plunging_attack: bool=False, is_charged_attack: bool=False):
        game.current_damage = cls(damage_type, main_damage_element, main_damage, piercing_damage, is_plunging_attack, is_charged_attack)

    # @staticmethod
    def resolve_damage(game: GeniusGame,
                    damage_type: SkillType, main_damage_element: ElementType, 
                    main_damage: int, piercing_damage: int,
                    damage_from: Entity, damage_to: Entity,
                    is_plunging_attack: bool=False, is_charged_attack: bool=False):    
        Damage.create_damage(game, damage_type, main_damage_element, 
                             main_damage, piercing_damage, 
                             damage_from, damage_to, 
                             is_plunging_attack, is_charged_attack)
        game.current_damage.cal_damage(game)
        game.current_damage.execute_damage(game)
        game.current_damage.after_damage(game)
    
    def after_damage(self, game: GeniusGame):
    #     # 扩散伤害
        if self.reaction is Swirl:
            Damage.resolve_damage(game, SkillType.OTHER, self.swirl_crystalize_type, 1, 0)
    #     pass
    def execute_damage(self, game: GeniusGame):
        # 打出伤害

        # TODO: 盾
        pass
    def cal_damage(self, game: GeniusGame):
        # 元素类型转化
        '''
        Based on my activeZone.
        '''
        # 元素反应
        '''
        Based on elemental Reation.
        '''
        self.Elemental_Reaction(game)
        # TODO: 可能产生新的独立伤害（扩散), 这一部分需要在当前伤害结算完毕后再进行
        
        # 伤害加算
        '''
        '''
        pass

    def Elemental_Reaction(self, game:GeniusGame):
        '''
        It will update game.current_damage, .
        '''
        damage = game.current_damage
        targetplay_id = 1 - game.active_player
        defenderActiveZone = game.players[targetplay_id].active_zone
        Reaction = None
        Swirl_Crystalize_type = None
        target_index = defenderActiveZone.active_idx + damage.target_idx_bias
        if target_index > defenderActiveZone.number_of_characters:
            target_index -= defenderActiveZone.number_of_characters

        # No attachment on Target
        if len(defenderActiveZone.character_list[target_index].element_attach) == 0:
            match damage.main_damage_element:
                case ElementType.CRYO | ElementType.HYDRO | ElementType.PYRO | ElementType.ELECTRO:
                    defenderActiveZone.character_list[target_index].element_attach.insert(0, damage.main_damage_element)
                case ElementType.DENDRO:
                    defenderActiveZone.character_list[target_index].element_attach.append(damage.main_damage_element)
            self.reaction = None
            self.swirl_crystalize_type = None
            return


        targetAttachElement = defenderActiveZone.character_list[target_index].element_attach[0]
    
        match damage.main_damage_element:
            case ElementType.CRYO: # 冰
                match targetAttachElement:
                    case ElementType.HYDRO: # 水
                        game.current_damage.main_damage += 1
                        Frozen(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Frozen
                    case ElementType.PYRO: # 火
                        game.current_damage.main_damage += 2
                        Melt(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Melt
                    case ElementType.ELECTRO:
                        game.current_damage.main_damage += 1
                        game.current_damage.piercing_damage += 1
                        Super_Conduct(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Super_Conduct
            case ElementType.HYDRO: # 水
                match targetAttachElement:
                    case ElementType.CRYO:
                        game.current_damage.main_damage += 1
                        Frozen(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Frozen
                    case ElementType.PYRO:
                        game.current_damage.main_damage += 2
                        Vaporize(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Vaporize
                    case ElementType.ELECTRO:
                        game.current_damage.main_damage += 1
                        game.current_damage.piercing_damage += 1
                        Electro_Charged(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Electro_Charged
                    case ElementType.DENDRO:
                        game.current_damage.main_damage += 1
                        Bloom(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Bloom
            case ElementType.PYRO: # 火
                match targetAttachElement:
                    case ElementType.CRYO: 
                        game.current_damage.main_damage += 2
                        Melt(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Frozen
                    case ElementType.HYDRO:
                        game.current_damage.main_damage += 2
                        Vaporize(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Vaporize
                    case ElementType.ELECTRO:
                        game.current_damage.main_damage += 2
                        Overload(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Overload
                    case ElementType.DENDRO:
                        game.current_damage.main_damage += 1
                        Burning(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Burning

            case ElementType.ELECTRO: # 雷
                match targetAttachElement:
                    case ElementType.CRYO:
                        game.current_damage.main_damage += 1
                        game.current_damage.piercing_damage += 1
                        Super_Conduct(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Super_Conduct
                    case ElementType.HYDRO:
                        game.current_damage.main_damage += 1
                        game.current_damage.piercing_damage += 1
                        Electro_Charged(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Electro_Charged
                    case ElementType.PYRO:
                        game.current_damage.main_damage += 2
                        Overload(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Overload
                    case ElementType.DENDRO:
                        game.current_damage.main_damage += 1
                        Quicken(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Quicken
                
            case ElementType.DENDRO: # 草
                match targetAttachElement:
                    case ElementType.HYDRO:
                        game.current_damage.main_damage += 1
                        Bloom(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Bloom
                    case ElementType.PYRO:
                        game.current_damage.main_damage += 1
                        Burning(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Burning
                    case ElementType.ELECTRO:
                        game.current_damage.main_damage += 1
                        Quicken(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Quicken
            
            case ElementType.ANEPMO: # 风
                match targetAttachElement:
                    case ElementType.CRYO | ElementType.HYDRO | ElementType.PYRO | ElementType.ELECTRO:
                        Swirl(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Swirl
                        Swirl_Crystalize_type = targetAttachElement

            case ElementType.GEO: # 岩
                match targetAttachElement:
                    case ElementType.CRYO | ElementType.HYDRO | ElementType.PYRO | ElementType.ELECTRO:
                        game.current_damage.main_damage += 1
                        Crystalize(game, targetplay_id, target_index)
                        Reaction = ElementalReactionType.Crystalize
                        Swirl_Crystalize_type = targetAttachElement
        if Reaction is None:
            match damage.main_damage_element:
                case ElementType.CRYO | ElementType.HYDRO | ElementType.PYRO | ElementType.ELECTRO:
                    if not damage.main_damage_element in defenderActiveZone.character_list[target_index].element_attach:
                        defenderActiveZone.character_list[target_index].element_attach.insert(0, damage.main_damage_element)
                case ElementType.DENDRO:
                    if not damage.main_damage_element in defenderActiveZone.character_list[target_index].element_attach:
                        defenderActiveZone.character_list[target_index].element_attach.append(damage.main_damage_element)

        self.reaction = Reaction
        self.swirl_crystalize_type = Swirl_Crystalize_type 