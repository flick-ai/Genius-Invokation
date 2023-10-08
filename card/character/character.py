from card.character.base import *

class Fischl(CharacterCard):
    ''' 菲谢尔 '''
    id: int = 0
    name: str = 'Fischl'
    element: ElementType = ElementType.ELECTRO
    weapon_tpye: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.MONDSTADT
    health_point: int = 10


    class NormalAttack(CharacterSkill):
        id: int = 0
        name: str = 'Bolts of Downfall'
        type: SkillType = SkillType.NORMAL_ATTACK

        # damage
        damage_type: SkillType = SkillType.NORMAL_ATTACK
        main_damage_element: ElementType = ElementType.ELECTRO
        main_damage: int = 2
        piercing_damage: int = 0

        # cost
        cost = [
            {
                'cost_num': 1,
                'cost_type': CostType.ELECTRO
            },
            {
                'cost_num': 2,
                'cost_type': CostType.BLACK
            }
        ]
       
        # @classmethod
        # def on_call(cls, game: GeniusGame):

        #     demage: Damage = Damage(cls.damage_type, cls.main_damage_element, cls.main_damage, cls.piercing_damage)

        #     pass

        
    
    class ElementalSkill(CharacterSkill):
        id: int = 1
        name: str = 'Nightrider'
        type: SkillType = SkillType.ELEMENTAL_SKILL
        demage: Damage = Damage(SkillType.ELEMENTAL_SKILL, ElementType.ELECTRO, 1, 0)

    class ElementalBrust(CharacterSkill):
        id: int = 2
        name: str
        type: SkillType = SkillType.ELEMENTAl_BURST
        demage: Damage = Damage(SkillType.ELEMENTAl_BURST, ElementType.ELECTRO, 4, 2)
        

    # def __init__(self) -> None:
    #     super().__init__()
    #     self.id = 0
    #     self.name = 'Fischl'
    #     self.element = ElementType.ELECTRO
    #     self.weapon_type = 1