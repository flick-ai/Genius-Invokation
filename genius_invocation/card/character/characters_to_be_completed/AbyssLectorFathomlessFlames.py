from genius_invocation.card.character.import_head import *


class AbyssLectorFathomlessFlames(Character):
    id: int = 2302
    name: str = "Abyss Lector: Fathomless Flames"
    name_ch = "深渊咏者·渊火"
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 6
    max_health_point: int = 6
    skill_list: List = []
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
