from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from typing import TYPE_CHECKING
from utils import *
if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer

def layout(game: 'GeniusGame'):
    layout = Layout()
    layout.split_column(
    Layout(name="upper"),
    Layout(name="lower")
    )

    layout["lower"].split_row(
        Layout(name="card"),
        Layout(name="support"),
        Layout(name="character"),
        Layout(name="summon"),
        Layout(name="dice")
    )
    layout["lower"]['card'].size = None
    layout["lower"]['card'].ratio = 1
    layout["lower"]['summon'].size = None
    layout["lower"]['summon'].ratio = 2
    layout["lower"]['character'].size = None
    layout["lower"]['character'].ratio = 5
    layout["lower"]['support'].size = None
    layout["lower"]['support'].ratio = 2
    layout["lower"]['dice'].size = None
    layout["lower"]['dice'].ratio = 1

    layout['lower']['card'].update(get_card(game.players[1]))

    layout["lower"]['dice'].update(get_dice(game.players[1]))
    layout['lower']['support'].update(get_support(game.players[1]))
    layout['lower']['summon'].update(get_summon(game.players[1]))
    return layout

def get_card(player: 'GeniusPlayer'):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    sponsor_message.add_column(style="blue", justify="right")
    if player.hand_zone.num() != 0:
        for card in player.hand_zone.card:
            sponsor_message.add_row(
                card.name,
                style='blue',
            )
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="SupportZone",
    )
    return message_panel

def get_summon(player: 'GeniusPlayer'):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    sponsor_message.add_column(style="blue", justify="right")
    if player.summon_zone.num() != 0:
        for summon in player.summon_zone.space:
            sponsor_message.add_row(
                summon.name,
                style='blue',
            )
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="SupportZone",
    )
    return message_panel


def get_support(player: 'GeniusPlayer'):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    sponsor_message.add_column(style="blue", justify="right")
    if player.support_zone.num() != 0:
        for support in player.support_zone.space:
            sponsor_message.add_row(
                support.name,
                style='blue',
            )

    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="SupportZone",
    )
    return message_panel

def get_summon(player: 'GeniusPlayer'):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    sponsor_message.add_column(style="blue", justify="right")
    if player.summons_zone.num() != 0:
        for summon in player.summons_zone.space:
            sponsor_message.add_row(
                summon.name,
                style='blue',
            )

    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="SupportZone",
    )
    return message_panel

def get_dice(player: 'GeniusPlayer'):
    sponsor_message = Table.grid()
    sponsor_message.add_column(style="blue", justify="right")
    if player.dice_zone.show() is not None:
        for dice in player.dice_zone.show():
            sponsor_message.add_row(
                DiceType(dice).name,
                style='blue',
            )

    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
            vertical="middle",
        ),
        title="DiceZone",
    )
    return message_panel