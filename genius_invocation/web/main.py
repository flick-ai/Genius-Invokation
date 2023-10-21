
from genius_invocation.web.game.game import GeniusGame
from genius_invocation.web.game.action import *
from genius_invocation.utils import *
from genius_invocation.user_layout import layout
from genius_invocation.web.utils_dict import get_dict
import js

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
        js.document.getElementById('information').innerText = game_inf_str
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
            for idx, item in enumerate(dice_zone):
                js.document.getElementById(f'{player}_dice{idx}').innerText = item
            character_zone = message[i]['character_zone']
            characters = [js.document.getElementsByClassName(f'character{i} {player}')[0] for i in range(3)]
            for idx, item in enumerate(character_zone):
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