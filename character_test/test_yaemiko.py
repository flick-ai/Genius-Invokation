"""
game_version: 4.1
card_involved: 
- Yae Miko
- Bennett
- Gambler's Earrings 
- Covenant of Rock
"""

#天狐霆雷击倒对方角色，触发赌徒的耳环回费，应不能使用磐岩盟契

#目前的代码实现，在角色死亡，选择下一个出战角色时会强制询问命令行用户，
#因此这里用超载强制切人来跳过此询问
import unittest
from typing import List, Dict, Tuple, Optional, Union

from test_base import TestBase
from test_utils import *
from genius_invocation.game.action import *

class TestYaeGamblerConvernant(TestBase, unittest.TestCase):
    player0_deck: Dict[str, List[str]] = {
        'character': ['Bennett', 'Yae_Miko', 'Arataki_Itto'],
        'action_card': ["GamblersEarrings"] * 29 + ["Covenant_of_Rock"]
    }
    player1_deck: Dict[str, List[str]] = {
        'character': ['Rhodeia_of_Loch', 'Bennett', 'Fischl'],
        'action_card': ['Timmie'] * 30
    }
    is_omni = True

    def test(self):
        self.initialize_game()
        player0_actions = [
            choose_cards_empty(),#初始换牌
            choose_character(0),#选择出战角色0
            #第1回合
            choose_dice_empty(),#投掷骰子
            Action(11, 0, [0, 1, 2]),#E
            Action(10, 0, [0, 1, 2]),#A
            end_round(),#结束回合
        ]
        self.run_actions_for_player(player0_actions, 0)
        self.assertEqual(self.game.players[1].character_list[0].health_point, 5)

        player0_actions = [
            #第2回合
            choose_dice_empty(),#投掷骰子
            Action(14, 3, [0]),#切换至角色1
            Action(11, 0, [0, 1, 2]),#E
            Action(10, 0, [0, 1, 2]),#A
            end_round(),#结束回合
            #第3回合
            choose_dice_empty(),#投掷骰子
        ]
        player1_actions = [
            #第2回合
            choose_dice_empty(),#投掷骰子
            Action(14, 3, [0]),#切换至角色1
            end_round(),#结束回合
            #第3回合
            choose_dice_empty(),#投掷骰子
        ]
        self.run_actions_double(player0_actions, player1_actions)
        self.assertEqual(self.game.players[1].character_list[0].health_point, 5)
        self.assertEqual(self.game.players[1].character_list[1].health_point, 8)
        player0_actions = [
            Action(10, 0, [0, 1, 2]),#A
            Action(0, 2, [0]),#给角色0装备赌徒的耳环
            Action(0, 3, [0]),#给角色1（八重神子）装备赌徒的耳环
            Action(12, 0, [0, 1, 2]),#Q
        ]
        player1_actions = [
            Action(10, 0, [0, 1, 2]),#A
            Action(10, 0, [0, 1, 2]),#A
            Action(14, 2, [0]),#切换至角色0
        ]
        self.run_actions_double(player0_actions, player1_actions)
        #此时应不能打出磐岩盟契
        self.assertEqual(self.game.active_player.action_mask[6][1][0], 0)
        #确认击杀
        self.assertEqual(self.game.players[1].character_list[0].is_alive, False)
        #前台的赌徒触发，而后台的赌徒不触发，回2费
        self.assertEqual(self.game.players[0].dice_zone.num(), 2)


if __name__ == '__main__':
    unittest.main()
        