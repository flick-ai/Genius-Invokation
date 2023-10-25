from genius_invocation.card.character.import_head import *


class MaguuKenki(Character):
    id: int = 2501
    name: str = "Maguu Kenki"
    name_ch = "魔偶剑鬼"
    element: ElementType = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = []
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
