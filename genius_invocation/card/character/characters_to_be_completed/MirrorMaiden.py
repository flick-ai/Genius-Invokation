from genius_invocation.card.character.import_head import *


class MirrorMaiden(Character):
    id: int = 2202
    name: str = "Mirror Maiden"
    name_ch = "愚人众·藏镜仕女"
    element: ElementType = ElementType.HYDRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.FATUI
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = []
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
