from rich import box
from rich import print
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from typing import TYPE_CHECKING
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer
from genius_invocation.entity.status import Shield
from loguru import logger

CHANGE_STYLE = 'green'
ACTIVE_PLAYER_STYLE = 'red'
ACTIVE_CHARACTER_STYLE = 'red'
OTHER_STYLE = 'white'


def layout(game: 'GeniusGame', base=None):
    print(base)
    layout = Layout()
    layout.split_column(
        Layout(name="Game", ratio=1),
        Layout(name="player0", ratio=4),
        Layout(name="player1",ratio=4),
        Layout(name="Input Action", ratio=2),
    )
    layout['Game'].update(get_game_info(game))
    layout['Input Action'].split_row(
        Layout(name="Action", ratio=1),
        Layout(name="SKill", ratio=1),
    )
    get_skill(layout['Input Action']['SKill'], game)
    for i in range(2):
        player = "player" + str(i)
        layout[player].split_row(
            Layout(name="card", ratio=2),
            Layout(name="support", ratio=3),
            Layout(name="character", ratio=6),
            Layout(name="summon", ratio=3),
            Layout(name="dice", ratio=1)
        )

        layout[player]['support'].split_column(Layout(name="12"),Layout(name="34"),)
        layout[player]['support']['12'].split_row(get_support(game.players[i], 0, base),get_support(game.players[i], 1, base))
        layout[player]['support']['34'].split_row(get_support(game.players[i], 2, base),get_support(game.players[i], 3, base))
        layout[player]['summon'].split_column(Layout(name="12"),Layout(name="34"),)

        layout[player]['summon']['12'].split_row(get_summon(game.players[i], 0, base),get_summon(game.players[i], 1, base))
        layout[player]['summon']['34'].split_row(get_summon(game.players[i], 2, base),get_summon(game.players[i], 3, base))

        layout[player]['character'].split_row(get_character(game.players[i], 0, base),
                                                 get_character(game.players[i], 1, base),
                                                 get_character(game.players[i], 2, base))

        layout[player]['card'].split_column(
            Layout(name="cards", ratio=1),
            Layout(name="hands", ratio=3),
        )
        layout[player]['card']['cards'].update(get_card(game.players[i]))
        layout[player]['card']['hands'].update(get_hand(game.players[i]))

        layout[player]['dice'].update(get_dice(game.players[i]))
    return layout

def get_game_info(game: 'GeniusGame'):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    sponsor_message.add_row(
        f"Round:{game.round}, Round_Phase:{game.game_phase.value}, Active_player:{game.active_player_index}, First_player:{game.first_player}",
        style='white',
    )
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="Game Information",
    )
    return message_panel

def print_prompt(layout, history, string):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)

    for his in history:
        sponsor_message.add_row(
        his,
        style=ACTIVE_PLAYER_STYLE,
    )
    sponsor_message.add_row(
        string,
        style=OTHER_STYLE,
    )
    message_panel = Panel(
                Align.center(
                    Group(" ",Align.center(sponsor_message)),
                    vertical="middle",
                    ),
                title="Input",
                style=OTHER_STYLE,
        )
    layout['Input Action']['Action'].update(message_panel)
    print(layout)

def get_skill(layout, game: 'GeniusGame'):
    if not game.active_player.active_idx in range(len(game.active_player.character_list)):
        sponsor_message = Table.grid()
        sponsor_message.add_column(no_wrap=True, justify="medium")
        sponsor_message.add_row(
            "No skill can be used",
            style='red',
        )
        message_panel = Panel(
                    Align.center(
                        Group(" ",Align.center(sponsor_message)),
                        vertical="middle",
                        ),
                    title="Skill",
                    style=OTHER_STYLE,
            )
        layout.update(message_panel)
    else:
        message_panel_list = []
        if game.active_player.character_list[game.active_player.active_idx].character_zone.special_skill != None:
            skill = game.active_player.character_list[game.active_player.active_idx].character_zone.special_skill
            sponsor_message = Table.grid()
            sponsor_message.add_column(no_wrap=True, justify="medium")
            sponsor_message.add_row(
                skill.name_ch,
                style='white',
            )
            sponsor_message.add_row(
                SkillToChinese(skill.type),
                style='white',
            )
            sponsor_message.add_row(
                CostToStr(skill.cost),
                style='white',
            )
            message_panel = Panel(
                    Align.center(
                        Group(" ",Align.center(sponsor_message)),
                        vertical="middle",
                        ),
                    title="Skill"+str(len(message_panel_list)),
                    style=OTHER_STYLE,
            )
            message_panel_list.append(message_panel)
        for skill in game.active_player.character_list[game.active_player.active_idx].skill_list:
            sponsor_message = Table.grid()
            sponsor_message.add_column(no_wrap=True, justify="medium")
            sponsor_message.add_row(
                skill.name_ch,
                style='white',
            )
            sponsor_message.add_row(
                SkillToChinese(skill.type),
                style='white',
            )
            sponsor_message.add_row(
                CostToStr(skill.cost),
                style='white',
            )
            message_panel = Panel(
                    Align.center(
                        Group(" ",Align.center(sponsor_message)),
                        vertical="middle",
                        ),
                    title="Skill"+str(len(message_panel_list)),
                    style=OTHER_STYLE
            )
            message_panel_list.append(message_panel)
        num = len(message_panel_list)
        if num == 3:
            layout.split_row(
                Layout(name="Skill1", ratio=1),
                Layout(name="Skill2", ratio=1),
                Layout(name="Skill3", ratio=1),
            )
            layout['Skill1'].update(message_panel_list[0])
            layout['Skill2'].update(message_panel_list[1])
            layout['Skill3'].update(message_panel_list[2])
        elif num == 4:
            layout.split_row(
                Layout(name="Skill1", ratio=1),
                Layout(name="Skill2", ratio=1),
                Layout(name="Skill3", ratio=1),
                Layout(name="Skill4", ratio=1),
            )
            layout['Skill1'].update(message_panel_list[0])
            layout['Skill2'].update(message_panel_list[1])
            layout['Skill3'].update(message_panel_list[2])
            layout['Skill4'].update(message_panel_list[3])
        elif num == 5:
            layout.split_row(
                Layout(name="Skill1", ratio=1),
                Layout(name="Skill2", ratio=1),
                Layout(name="Skill3", ratio=1),
                Layout(name="Skill4", ratio=1),
                Layout(name="Skill5", ratio=1),
            )
            layout['Skill1'].update(message_panel_list[0])
            layout['Skill2'].update(message_panel_list[1])
            layout['Skill3'].update(message_panel_list[2])
            layout['Skill4'].update(message_panel_list[3])
            layout['Skill5'].update(message_panel_list[4])


def get_character(player: 'GeniusPlayer', idx: int, base=None):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=False, justify="medium")
    character_list = player.character_list
    if idx >= len(character_list):
        message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
            vertical="middle",
        ),
        title="Character",
        )
        return message_panel        
    
    if character_list[idx].is_active:
        color = ACTIVE_CHARACTER_STYLE
    else:
        color = OTHER_STYLE
    if character_list[idx].is_alive:
        col = OTHER_STYLE
        if len(character_list[idx].elemental_application)>0:
            col = ElementsToColor(character_list[idx].elemental_application[0])
        sponsor_message.add_row(
            Elementals_to_str(character_list[idx].elemental_application),
            style=col,
        )
        sponsor_message.add_row(
            character_list[idx].name_ch,
            style=color,
        )
        sponsor_message.add_row(
            character_list[idx].show(),
            style=color,
        )
        sponsor_message.add_row(
            str(character_list[idx].power),
            style=color,
        )

        if character_list[idx].character_zone.weapon_card != None:
            sponsor_message.add_row(
                character_list[idx].character_zone.weapon_card.show(),
                style=color,
            )
        if character_list[idx].character_zone.artifact_card != None:
            sponsor_message.add_row(
                character_list[idx].character_zone.artifact_card.show(),
                style=color,
            )
        if character_list[idx].talent == True:
            sponsor_message.add_row(
                f"Has Talent",
                style=color,
            )
        # if character_list[idx].character_zone.special_skill != None:
        #     sponsor_message.add_row(
        #     character_list[idx].character_zone.special_skill.show(),
        #     style=color,
        # )
        for status in character_list[idx].character_zone.status_list:
            if isinstance(status, Shield):
                col = 'yellow'
            else:
                col='blue'
            sponsor_message.add_row(
                f"{status.name_ch}: {status.show()}",
                style=col,
            )
        if character_list[idx].is_active:
            for status in player.team_combat_status.shield:
                sponsor_message.add_row(
                    f"{status.name_ch}:{status.show()}",
                    style='yellow',
                )
            for status in player.team_combat_status.space:
                sponsor_message.add_row(
                    f"{status.name_ch}:{status.show()}",
                    style='blue',
                )

    if player.index == player.game.active_player_index:
        style = ACTIVE_PLAYER_STYLE
    else:
        style = OTHER_STYLE
    if base is not None:
        for diff in base:
            if diff[0] == player.index and diff[1] == ZoneType.CHARACTER_ZONE and diff[2] == idx:
                style = CHANGE_STYLE
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
            vertical="middle",
        ),
        title="Character"+str(idx),
        style=style,
    )
    return message_panel

def get_card(player: 'GeniusPlayer'):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    sponsor_message.add_row(
        str(player.card_zone.num()),
        style=OTHER_STYLE,
    )

    if player.index == player.game.active_player_index:
        style = ACTIVE_PLAYER_STYLE
    else:
        style = OTHER_STYLE
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="CardZone",
        style=style,
    )
    return message_panel

def get_hand(player: 'GeniusPlayer'):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    if player.hand_zone.num() != 0:
        for card in player.hand_zone.card:
            sponsor_message.add_row(
                "{}:{}".format(CostToStr(card.calculate_cost()), card.name_ch),
                style='white',
            )

    if player.index == player.game.active_player_index:
        style = ACTIVE_PLAYER_STYLE
    else:
        style = OTHER_STYLE
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="HandCard"+str(player.index),
        style=style,
    )
    return message_panel

def get_summon(player: 'GeniusPlayer', idx, base=None):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    if player.summon_zone.num() > idx:
        summon = player.summon_zone.space[idx]
        try:
            this_element = summon.infuse_element
        except:
            this_element = summon.element
        sponsor_message.add_row(
            summon.name_ch,
            style=ElementsToColor(this_element),
        )
        sponsor_message.add_row(
            str(summon.show()),
            style=ElementsToColor(this_element),
        )

    if player.index == player.game.active_player_index:
        style = ACTIVE_PLAYER_STYLE
    else:
        style = OTHER_STYLE
    if base is not None:
        for diff in base:
            if diff[0] == player.index and diff[1] == ZoneType.SUMMON_ZONE and diff[2] == idx:
                style = CHANGE_STYLE
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="Summon"+str(idx+1),
        style=style,
    )
    return message_panel


def get_support(player: 'GeniusPlayer', idx, base=None):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    if player.support_zone.num() > idx:
        support = player.support_zone.space[idx]
        sponsor_message.add_row(
            support.name_ch,
            style='blue',
        )
        sponsor_message.add_row(
            support.show(),
            style='blue',
        )

    if player.index == player.game.active_player_index:
        style = ACTIVE_PLAYER_STYLE
    else:
        style = OTHER_STYLE
    if base is not None:
        for diff in base:
            if diff[0] == player.index and diff[1] == ZoneType.SUPPORT_ZONE and diff[2] == idx:
                style = CHANGE_STYLE
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="Support" + str(idx),
        style=style,
    )
    return message_panel

def get_dice(player: 'GeniusPlayer'):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    if player.dice_zone.show() is not None:
        for dice in player.dice_zone.show():
            sponsor_message.add_row(
                DiceToChinese(DiceType(dice)),
                style=DiceToColor(DiceType(dice)),
            )
    
    if player.index == player.game.active_player_index:
        style = ACTIVE_PLAYER_STYLE
    else:
        style = OTHER_STYLE
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
            vertical="middle",
        ),
        title="Dice"+str(player.index),
        style=style,
    )
    return message_panel