
from genius_invocation.web.game.game import GeniusGame
from genius_invocation.web.game.action import *
from genius_invocation.utils import *
import genius_invocation.card.action as actioncard
from genius_invocation.user_layout import layout
from genius_invocation.web.utils_dict import get_dict
import js
from pyodide import create_proxy

from genius_invocation.web.get_card import get_card

import inspect



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

    get_card()

    available_card = []
    ignore = [actioncard.ActionCard, actioncard.EquipmentCard, actioncard.WeaponCard, actioncard.TalentCard, actioncard.ArtifactCard, actioncard.SupportCard, actioncard.FoodCard]
    for name, obj in inspect.getmembers(actioncard):
        if inspect.isclass(obj) and obj not in ignore:
            available_card.append((name, obj.name, obj.name_ch, obj))

    
    

    # js_available_card = {available_card[i][2]: available_card[i][0] for i in range(len(available_card))}
    # js.load_action_cards(create_proxy(js_available_card))
    select = []
    cur_idx = 0
    while True:
        await asyncio.sleep(0.1)
        if js.document.getElementById('currentselect').innerText != '':
            select.append(js.document.getElementById('currentselect').innerText.split(' '))
            js.document.getElementById('currentselect').innerText = ''
            current_available_card = select_card(select[cur_idx], available_card)
            js.load_action_cards(create_proxy(current_available_card))
            cur_idx += 1
        if cur_idx == 2:
            for item in js.document.getElementsByClassName('before'):
                item.style.display = 'none'
            break
    
    print(select)
    deck1 = {
    'character': select[0],
    'action_card': ['Fresh_Wind_of_Freedom','Dunyarzad','Dunyarzad','Chef_Mao','Chef_Mao','Paimon','Paimon',
                    'Rana','Rana','Liben','Liben','Mushroom_Pizza','Mushroom_Pizza','Adeptus_Temptation',
                    'Adeptus_Temptation','Teyvat_Fried_Egg','Sweet_Madame','Sweet_Madame','Mondstadt_Hash_Brown',
                    'Lotus_Flower_Crisp','Lotus_Flower_Crisp','Strategize','Strategize','Leave_it_to_Me','Leave_it_to_Me',
                    'PaidinFull','PaidinFull','Send_Off','Starsigns','Starsigns']
    }
    deck2 = {
    'character': select[1],
    'action_card': ['Tenacity_of_the_Millelith','Tenacity_of_the_Millelith','TheBell','TheBell','Paimon','Paimon',
                    'Chef_Mao','Chef_Mao','Liben','Liben','Dunyarzad','Dunyarzad','Fresh_Wind_of_Freedom',
                    'Woven_Stone','Woven_Stone','Enduring_Rock','Enduring_Rock','Strategize','Strategize',
                    'Leave_it_to_Me','Send_Off','Heavy_Strike','Heavy_Strike','Adeptus_Temptation',
                    'Lotus_Flower_Crisp','Lotus_Flower_Crisp','Sweet_Madame','Mondstadt_Hash_Brown',
                    'Mushroom_Pizza','Mushroom_Pizza']
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
            js.document.getElementsByClassName(f'player{i}box')[0].style.borderColor = '#DDDDDD'
        js.document.getElementsByClassName(f'player{active_player}box')[0].style.borderColor = '#EE6622'
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

            card_num = message[i]['card_zone']
            card_num_place = js.document.getElementsByClassName(f'cardzone {player}')[0]
            card_num_place = card_num_place.getElementsByClassName('thetitle')[1]
            card_num_place.innerText = f'{card_num}'

            # 召唤物区
            summon_zone = message[i]['summon_zone']
            for idx in range(4):
                summon = js.document.getElementsByClassName(f'summon{idx} {player}')[0]
                summon.getElementsByClassName('thetitle')[0].innerText = f'召唤区{idx+1}'
                summon.getElementsByClassName('inneritem')[0].innerText = ''
            for idx, item in enumerate(summon_zone):
                summon = js.document.getElementsByClassName(f'summon{idx} {player}')[0]
                summon.getElementsByClassName('thetitle')[0].innerText = item[0]
                summon.getElementsByClassName('inneritem')[0].innerText = item[1]

            # 支援区
            support_zone = message[i]['support_zone']
            for idx in range(4):
                support = js.document.getElementsByClassName(f'support{idx} {player}')[0]
                support.getElementsByClassName('thetitle')[0].innerText = f'支援区{idx+1}'
                support.getElementsByClassName('inneritem')[0].innerText = ''
            for idx, item in enumerate(support_zone):
                support = js.document.getElementsByClassName(f'support{idx} {player}')[0]
                support.getElementsByClassName('thetitle')[0].innerText = item[0]
                support.getElementsByClassName('inneritem')[0].innerText = item[1]

            # 角色区
            character_zone = message[i]['character_zone']
            characters = [js.document.getElementsByClassName(f'character{j} {player}')[0] for j in range(3)]
            for idx, item in enumerate(character_zone):
                if item['base'][4]:
                    characters[idx].style.borderColor = '#994400'
                else:
                    characters[idx].style.borderColor = '#00000000'
                js.document.getElementById(f'{player}_character{idx}_element').style.background = element_to_dice[item['base'][0]]
                characters[idx].getElementsByClassName('thetitle')[0].innerText = item['base'][1]
                js.document.getElementById(f'{player}_character{idx}_health').innerText = item['base'][2]
                js.document.getElementById(f'{player}_character{idx}_power').innerText = item['base'][3]
                for skill_idx, skill in enumerate(item['skills']):
                    js.document.getElementById(f'{player}_character{idx}_skill{skill_idx}').innerText = skill

                if len(item['status']) == 0:
                    chara_state = '角色状态\n(空)'
                else:
                    chara_state = '角色状态\n' + '\n'.join(item['status'])
                js.document.getElementById(f'{player}_character{idx}_state_inner').innerText = chara_state

                if item['active'] == "Active":
                    js.document.getElementById(f'{player}_character{idx}_group_state').style.display = 'inline-block'
                    if len(item['shield']) == 0:
                        shield_state = '护盾\n(空)'
                    else:
                        shield_state = '护盾\n' + '\n'.join(item['shield'])
                    if len(item['active_status']) == 0:
                        active_state = '出战状态\n(空)'
                    else:
                        active_state = '出战状态\n' + '\n'.join(item['active_status'])
                    js.document.getElementById(f'{player}_character{idx}_group_state_inner').innerText = shield_state +'\n' + active_state
                else:
                    js.document.getElementById(f'{player}_character{idx}_group_state').style.display = 'none'
            


        action = await from_input(game)
        game.step(action)

    print_information(information)

if __name__ == '__main__':
    main()