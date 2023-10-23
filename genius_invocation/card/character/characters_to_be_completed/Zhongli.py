from genius_invocation.card.character.characters.import_head import *


class Zhongli(Character):
    id: int = 1603
    name: str = "Zhongli"
    name_ch = "钟离"
    element: ElementType = ElementType.GEO
    weapon_type: WeaponType = WeaponType.POLEARM
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = []
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
