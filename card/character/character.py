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
        demage: Damage = Damage()
        

    # def __init__(self) -> None:
    #     super().__init__()
    #     self.id = 0
    #     self.name = 'Fischl'
    #     self.element = ElementType.ELECTRO
    #     self.weapon_type = 1