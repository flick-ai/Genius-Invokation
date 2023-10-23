from genius_invocation.card.character.characters.import_head import *


class Ningguang(Character):
    id: int = 1601
    name: str = "Ningguang"
    name_ch = "凝光"
    element: ElementType = ElementType.GEO
    weapon_type: WeaponType = WeaponType.CATALYST
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = []
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
