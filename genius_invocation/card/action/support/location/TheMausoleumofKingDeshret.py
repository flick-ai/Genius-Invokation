from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support
from genius_invocation.entity.status import Combat_Status
from genius_invocation.event.damage import Damage
from genius_invocation.card.action.base import ActionCard


if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class HasForbiddenKnowledge(Combat_Status):
    name: str = 'Forbidden Knowledge'
    name_ch = '禁忌知识'
    id = 32102031
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_end(self, game:'GeniusGame'):
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.FINAL_END, ZoneType.ACTIVE_ZONE, self.on_end),
        ]

class ForbiddenKnowledge(ActionCard):
    name = "Forbidden Knowledge"
    name_ch = "禁忌知识"
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT
    can_tune = False
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        game.active_player.team_combat_status.add_entity(HasForbiddenKnowledge(game, game.active_player))
        dmg = Damage.create_damage(
            game,
            damage_type=SkillType.OTHER,
            main_damage_element=ElementType.PIERCING,
            main_damage=1,
            piercing_damage=0,
            damage_from=None,
            damage_to=get_my_active_character(game),
        )
        game.add_damage(dmg)
        game.resolve_damage()
        game.active_player.get_card(num=1)

    def on_tuning(self, game: 'GeniusGame') -> None:
        pass

    def find_target(self, game: 'GeniusGame'):
        if game.active_player.last_die_round == game.round :
            if game.active_player.team_combat_status.has_status(HasForbiddenKnowledge) is None:
                return [1]
        return []


class TheMausoleumofKingDeshretStatus(Combat_Status):
    name: str = 'The Mausoleum of King Deshret'
    name_ch = '赤王陵'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_get_card(self, game: 'GeniusGame'):
        if game.current_get_card.from_player == self.from_player:
            self.from_player.card_zone.insert_randomly([ForbiddenKnowledge()], num=-1)

    def on_end(self, game:'GeniusGame'):
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_PLAY_CARD, ZoneType.ACTIVE_ZONE, self.on_play),
            (EventType.FINAL_END, ZoneType.ACTIVE_ZONE, self.on_end),
        ]


class TheMausoleumofKingDeshretEntity(Support):
    name: str = 'The Mausoleum of King Deshret'
    name_ch = '赤王陵'
    id = 32102061
    max_count = 4
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.count = 0
        self.oppenent = get_opponent(game)

    def on_get_card(self, game: 'GeniusGame'):
        if game.current_get_card.from_player == self.oppenent:
            self.count += 1
            if self.count == self.max_count:
                self.on_destroy(game)
                for _ in range(2):
                    self.oppenent.card_zone.insert_randomly(ForbiddenKnowledge(), 0)
                self.oppenent.team_combat_status.add_entity(TheMausoleumofKingDeshretStatus(game, self.oppenent))

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_GET_CARD, ZoneType.SUPPORT_ZONE, self.on_get_card),
        ]

    def show(self):
        return str(self.count)

class TheMausoleumofKingDeshret(SupportCard):
    id: int = 321020
    name: str = 'The Mausoleum of King Deshret'
    name_ch = '赤王陵'
    time = 4.7
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = TheMausoleumofKingDeshretEntity(game, from_player=game.active_player)
        super().on_played(game)