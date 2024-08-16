from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.event.damage import Damage
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class WaterandJustice(ActionCard):
    id: int = 331805
    name: str = 'Water and Justice'
    name_ch = "水与正义"
    time = 4.7
    cost_num = 2
    cost_type = CostType.BLACK
    country = CountryType.FONTAINE
    card_type = ActionCardType.EVENT_COUNTRY

    def __init__(self) -> None:
        super().__init__()

    def calculate_target_point(self,sum_point: int, max_points: List[int]):
        # 计算重新平均分配生命值
        need_character = len(max_points)
        target_point = [0 for i in range(need_character)]
        target_idx = [i for i in range(need_character)]

        while sum_point > 0:
            for idx in target_idx:
                target_point[idx] += 1
                sum_point -= 1
                if sum_point == 0:
                    break
                if max_points[idx] == target_point[idx]:
                    target_idx.remove(idx)

        return target_point


    def on_played(self, game: 'GeniusGame'):
        sum_point = 0
        max_points = []
        character_list = [get_my_active_character(game)].extend(get_my_standby_character(game))
        for character in character_list:
            sum_point += character.health_point
            max_points.append(character.max_health_point)
        target_point = self.calculate_target_point(sum_point, max_points)

        # 进行对应操作
        for idx, character in enumerate(character_list):
            if target_point > character.health_point:
                character.heal(heal=target_point[idx]-character.health_point, game=game, heal_type=HealType.HEALTH_ASSIGNMENT)
            elif target_point < character.health_point:
                damage = Damage.create_damage(
                    game=game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.PIERCING,
                    main_damage=character.health_point-target_point[idx],
                    piercing_damage=0,
                    damage_from=None,
                    damage_to=character
                )
                game.add_damage(damage)
                game.resolve_damage()

            character.heal(heal=1, game=game)

