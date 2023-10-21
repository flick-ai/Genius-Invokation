
from genius_invocation.web.game.game import GeniusGame
from genius_invocation.web.game.action import *
from genius_invocation.utils import *
from genius_invocation.user_layout import layout
from genius_invocation.web.utils_dict import get_dict
import js


element_to_dice = {
    "CRYO": "rgb(153,255,255)",
    "HYDRO": "rgb(58,90,186)",
    "PYRO": "rgb(255,153,153)",
    "ELECTRO": "rgb(144,53,144)",
    "ANEMO": "rgb(128,255,215)",
    "GEO": "rgb(255,230,153)",
    "DENDRO": "rgb(126,194,54)",
    "None": "rgb(187, 187, 187)",
    "OMNI": "rgb(255,221,245)",
}

async def main():
    deck1 = {
    'character': ['Rhodeia_of_Loch', 'Nahida', 'Tartaglia'],
    'action_card': ['Liben' for i in range(30)]
    }
    deck2 = {
    'character': ['Cyno', 'Wanderer', 'Yoimiya'],
    'action_card': ['Liben' for i in range(30)]
    }
    game = GeniusGame(player0_deck=deck1, player1_deck=deck2)
    information = []

    while not game.is_end:
        message = get_dict(game)


        game_information = message['game']
        game_inf_str = f"回合: {game_information['round']}, 阶段: {game_information['round_phase']}, 当前玩家: {game_information['active_player']}, 先手玩家: {game_information['first_player']}"
        active_player = game_information['active_player']
        js.document.getElementById('information').innerText = game_inf_str
        for i in range(2):
            js.document.getElementsByClassName(f'player{i}')[0].style.borderColor = '#00000000'
        js.document.getElementsByClassName(f'player{active_player}')[0].style.borderColor = '#EE6622'
        # print(game.encode_message())
        print(message)
        for i, player in enumerate(['player0', 'player1']):
            hand_zone = message[i]['hand_zone']
            for idx in range(10):
                js.document.getElementById(f'{player}_card{idx}').innerText = ''
            for idx, item in enumerate(hand_zone):
                js.document.getElementById(f'{player}_card{idx}').innerText = item
            dice_zone = message[i]['dice_zone']
            for idx in range(16):
                js.document.getElementById(f'{player}_dice{idx}').innerText = ''
                js.document.getElementById(f'{player}_dice{idx}').style.background = '#00000000'
            for idx, item in enumerate(dice_zone):
                js.document.getElementById(f'{player}_dice{idx}').innerText = ''
                js.document.getElementById(f'{player}_dice{idx}').style.background = element_to_dice[item]
            character_zone = message[i]['character_zone']
            characters = [js.document.getElementsByClassName(f'character{i} {player}')[0] for i in range(3)]
            for idx, item in enumerate(character_zone):
                if item['base'][4]:
                    characters[idx].style.borderColor = '#994400'
                else:
                    characters[idx].style.borderColor = '#00000000'
                js.document.getElementById(f'{player}_character{idx}_element').style.background = element_to_dice[item['base'][0]]
                characters[idx].getElementsByClassName('title')[0].innerText = item['base'][1]
                js.document.getElementById(f'{player}_character{idx}_health').innerText = item['base'][2]
                js.document.getElementById(f'{player}_character{idx}_power').innerText = item['base'][3]
                for skill_idx, skill in enumerate(item['skills']):
                    js.document.getElementById(f'{player}_character{idx}_skill{skill_idx}').innerText = skill
            


        action = await from_input(game)
        game.step(action)

    print_information(information)

if __name__ == '__main__':
    main()