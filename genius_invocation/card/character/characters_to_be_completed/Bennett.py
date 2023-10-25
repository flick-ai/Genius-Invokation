from genius_invocation.card.character.import_head import *


class Bennett(Character):
    id: int = 1303
    name: str = "Bennett"
    name_ch = "班尼特"
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = []
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
