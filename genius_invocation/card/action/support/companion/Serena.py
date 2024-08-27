from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support
from genius_invocation.card.action import ActionCard
from genius_invocation.entity.status import Combat_Status
from genius_invocation.event.damage import Damage
import os
from copy import deepcopy

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class SerenaEntity(Support):
    id: int = 322027
    name: str = 'Serena'
    name_ch = '瑟琳'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.generate(game)

    def generate(self, game:'GeniusGame'):
        pass

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.generate(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]


class Serena(SupportCard):
    id: int = 322027
    name: str = 'Serena'
    name_ch = '瑟琳'
    time = 4.8
    cost_num = 2
    cost_type = CostType.BLACK
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = SerenaEntity(game, from_player=game.active_player)
        super().on_played(game)

class SerenaSupport(ActionCard):
    id: int = 32202770
    name: str = 'Serena'
    name_ch = '瑟琳的声援'
    time = 4.8
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()
        self.cards = []
        cards_dir = "./card/action/event/foods"
        available_name = [f[:-3] for f in os.listdir(cards_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
        self.cards.extend(available_name)

    def on_played(self, game: 'GeniusGame') -> None:
        cards = []
        for i in range(2):
            cards.append(random.choice(self.cards))
        game.active_player.hand_zone.add_card_by_name(cards)


class CosanzeanaSupport(ActionCard):
    id: int = 32202771
    name: str = 'Cosanzeana'
    name_ch = '柯莎的声援'
    time = 4.8
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()
        self.cards = []
        cards_dir = "./card/action/equipment/weapon/weapons"
        available_name = [f[:-3] for f in os.listdir(cards_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
        self.cards.extend(available_name)

    def on_played(self, game: 'GeniusGame') -> None:
        cards = []
        for i in range(2):
            cards.append(random.choice(self.cards))
        game.active_player.hand_zone.add_card_by_name(cards)


class LaumeSupport(ActionCard):
    id: int = 32202772
    name: str = 'Laume'
    name_ch = '洛梅的声援'
    time = 4.8
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()
        self.cards = []
        cards_dir = "./card/action/equipment/artifact/artifacts"
        available_name = [f[:-3] for f in os.listdir(cards_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
        self.cards.extend(available_name)

    def on_played(self, game: 'GeniusGame') -> None:
        cards = []
        for i in range(2):
            cards.append(random.choice(self.cards))
        game.active_player.hand_zone.add_card_by_name(cards)

class VirdaSupport(ActionCard):
    id: int = 32202773
    name: str = 'Virda'
    name_ch = '薇尔妲的声援'
    time = 4.8
    cost_num = 2
    cost_type = CostType.BLACK
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()
        self.cards = []
        cards_dir = "./card/action/event/arcane_legend"
        available_name = [f[:-3] for f in os.listdir(cards_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
        self.cards.extend(available_name)

    def on_played(self, game: 'GeniusGame') -> None:
        cards = []
        for i in range(2):
            cards.append(random.choice(self.cards))
        game.active_player.hand_zone.add_card_by_name(cards)
        game.active_player.play_arcane_legend = False

class SluasiSupport(ActionCard):
    id: int = 32202774
    name: str = 'Sluasi'
    name_ch = '希露艾的声援'
    time = 4.8
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        cards = get_opponent(game).card_zone.card[0:3]
        self.from_player.hand_zone.add([deepcopy(card) for card in cards])


class CanotilaSupport(ActionCard):
    id: int = 32202775
    name: str = 'Canotila'
    name_ch = '夏诺蒂拉的声援'
    time = 4.8
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()
        self.cards = []
        cards_dirs = ["./card/action/event/country_resonance",
                     "./card/action/event/elemental_resonance_event",]
        for cards_dir in cards_dirs:
            available_name = [f[:-3] for f in os.listdir(cards_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
            self.cards.extend(available_name)

    def on_played(self, game: 'GeniusGame') -> None:
        cards = []
        for i in range(2):
            cards.append(random.choice(self.cards))
        game.active_player.hand_zone.add_card_by_name(cards)

class ThironaEntity(Combat_Status):
    id: int = 32202736
    name: str = 'Thirona'
    name_ch = '希洛娜的声援'
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.cards = []
        cards_dirs = ["./card/action/event/country_resonance",
                     "./card/action/event/elemental_resonance_event",]
        for cards_dir in cards_dirs:
            available_name = [f[:-3] for f in os.listdir(cards_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
            self.cards.extend(available_name)

    def on_end(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            card = random.choice(self.cards)
            game.active_player.hand_zone.add_card_by_name(card)
            self.usage -= 1
            if self.usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.ACTIVE_ZONE, self.on_end),
        ]

class ThironaSupport(ActionCard):
    id: int = 32202776
    name: str = 'Thirona'
    name_ch = '希洛娜的声援'
    time = 4.8
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        game.active_player.team_combat_status.add_entity(ThironaEntity(
            game,
            from_player=game.active_player,
            from_character=None
        ))

class TopyasEntity(Combat_Status):
    id: int = 32202737
    name: str = 'Topyas'
    name_ch = '托皮娅的声援'
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def after_play_card(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            flag = random.random()
            if flag < 0.5:
                game.active_player.get_card(num=1)
            else:
                idx = random.randint(0, game.active_player.hand_zone.num()-1)
                game.active_player.hand_zone.discard_card(idx)

    def on_end(self, game:'GeniusGame'):
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.ACTIVE_ZONE, self.on_end),
            (EventType.AFTER_PLAY_CARD, ZoneType.ACTIVE_ZONE, self.after_play_card)
        ]

class TopyasSupport(ActionCard):
    id: int = 32202777
    name: str = 'Topyas'
    name_ch = '托皮娅的声援'
    time = 4.8
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        game.active_player.get_card(num=2)
        for player in game.players:
            player.team_combat_status.add_entity(TopyasEntity(
                game,
                from_player=game.active_player,
                from_character=None
            ))

class PucaSupport(ActionCard):
    id: int = 32202778
    name: str = 'Puca'
    name_ch = '芙佳的声援'
    time = 4.8
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()
        cards_dirs = ["./card/action/support/companion",
                      "./card/action/support/item",
                      "./card/action/support/location"]
        self.cards = []
        for package_dir in cards_dirs:
            available_name = [f[:-3] for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
            self.cards.extend(available_name)

    def on_played(self, game: 'GeniusGame') -> None:
        for player in game.players:
            generate_num = MAX_SUPPORT - player.support_zone.num()
            for i in range(generate_num):
                card_name = random.choice(self.cards)
                player.support_zone.add_card_by_name(card_name)

class LutineEntity(Combat_Status):
    id: int = 32202739
    name: str = 'Lutine'
    name_ch = '卢蒂尼的声援'
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def after_use_skill(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            flag = random.random()
            if flag < 0.5:
                get_my_active_character(game).heal(heal=2)
            else:
                dmg = Damage(
                    damage_type=SkillType.OTHER,
                    main_damage=2,
                    main_damage_element=ElementType.PIERCING,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_my_active_character(game)
                )
                game.add_damage(dmg)
                game.resolve_damage()

    def on_end(self, game:'GeniusGame'):
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.ACTIVE_ZONE, self.on_end),
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.after_use_skill)
        ]

class LutineSupport(ActionCard):
    id: int = 32202779
    name: str = 'Lutine'
    name_ch = '卢蒂尼的声援'
    time = 4.8
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        game.active_player.get_card(num=2)
        for player in game.players:
            player.team_combat_status.add_entity(LutineEntity(
                game,
                from_player=game.active_player,
                from_character=None
            ))




