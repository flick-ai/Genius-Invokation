from genius_invocation.card.character.characters.import_head import *


class YaeMiko(Character):
    id: int = 1408
    name: str = "Yae Miko"
    name_ch = "八重神子"
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.CATALYST
    country: CountryType = CountryType.INAZUMA
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = []
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
