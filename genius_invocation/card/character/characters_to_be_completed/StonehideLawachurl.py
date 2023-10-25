from genius_invocation.card.character.import_head import *


class StonehideLawachurl(Character):
    id: int = 2601
    name: str = "Stonehide Lawachurl"
    name_ch = "丘丘岩盔王"
    element: ElementType = ElementType.GEO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.HILICHURL
    init_health_point: int = 8
    max_health_point: int = 8
    skill_list: List = []
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
