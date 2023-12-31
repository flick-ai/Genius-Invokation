import unittest
from typing import List, Dict, Tuple, Optional, Union

from character_test.test_base import TestBase
from character_test.test_utils import *
from genius_invocation.game.action import *

'''Error
Traceback (most recent call last):
  File "E:\GitHub\Genius-Invokation\test\test_character_solo\test_solo_Mona.py", line 68, in test
    self.run_actions_for_player(skill_action_list[0], 0)  # 平a
  File "E:\GitHub\Genius-Invokation\test\test_base.py", line 83, in run_actions_for_player
    game.step(action)
  File "E:\GitHub\Genius-Invokation\genius_invocation\game\game.py", line 221, in step
    self.resolve_action(action)
  File "E:\GitHub\Genius-Invokation\genius_invocation\game\game.py", line 100, in resolve_action
    active_player.use_skill(self)
  File "E:\GitHub\Genius-Invokation\genius_invocation\game\player.py", line 165, in use_skill
    self.character_list[self.active_idx].skill(idx, game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\entity\character.py", line 91, in skill
    self.skills[skill].on_call(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\card\character\characters\Mona.py", line 36, in on_call
    self.resolve_damage(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\card\character\base.py", line 52, in resolve_damage
    game.resolve_damage()
  File "E:\GitHub\Genius-Invokation\genius_invocation\game\game.py", line 137, in resolve_damage
    self.current_damage.on_damage(self)
  File "E:\GitHub\Genius-Invokation\genius_invocation\event\damage\damage.py", line 60, in on_damage
    self.damage_dealing(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\event\damage\damage.py", line 78, in damage_dealing
    game.manager.invoke(EventType.DEALING_DAMAGE, game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\event\events.py", line 84, in invoke
    self.events[event_type](zone_type)(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\event\events.py", line 61, in __call__
    listener(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\event\events.py", line 23, in __call__
    self.action(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\card\character\characters\Mona.py", line 225, in on_dealing_damage
    game.current_damage *= 2
TypeError: unsupported operand type(s) for *=: 'Damage' and 'int'
'''

class TestMona(TestBase, unittest.TestCase):
    player0_deck: Dict[str, List[str]] ={
        'character': ['Mona'],
        'action_card': ['Thunder_and_Eternity'] * 30
    }
    player1_deck: Dict[str, List[str]] = {
        'character': ['Fischl', 'Cyno', 'Eula'],
        'action_card': ['Thunder_and_Eternity'] * 30
    }

    def test(self):
        # 用例初始化
        self.initialize_game()
        self.game.active_player_index = 0
        self.game.players[1].character_list[0].health_point = 100
        player0_init_actions = [
            choose_cards_empty(),  # 初始换牌
            choose_character(0),  # 选择出战角色
            choose_dice_empty(),  # 投掷骰子
            Action(0, 9, []),  # 打出雷与永恒
        ]
        player1_init_actions = [
            choose_cards_empty(),  # 初始换牌
            choose_character(0),  # 选择出战角色
            choose_dice_empty(),  # 投掷骰子
            Action(0, 9, []),  # 打出雷与永恒
        ]
        self.run_actions_for_player(player0_init_actions, 0)
        skill_action_list = [
            [Action(10, 0, [0, 1, 2])],
            [Action(11, 0, [0, 1, 2])],
            [Action(12, 0, [0, 1, 2])]
        ]

        # 用例执行 回合1:我方行动，对方空过 （伤害测试）
        self.run_actions_for_player(skill_action_list[0], 0)  # 平a
        self.check_health(1, [99, 10, 10])
        self.check_elemental_application(1, [[ElementType.HYDRO], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[1], 0)  # 第一个E技能
        self.check_health(1, [98, 10, 10])
        self.check_elemental_application(1, [[ElementType.HYDRO], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[1], 0)  # 第二个E技能，如果没有，则重复释放
        self.check_health(1, [97, 10, 10])
        self.check_elemental_application(1, [[ElementType.HYDRO], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[2], 0)  # Q技能
        self.check_health(1, [93, 10, 10])
        self.check_elemental_application(1, [[ElementType.HYDRO], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[0], 0)  # 平a
        self.check_health(1, [91, 10, 10])
        self.check_elemental_application(1, [[ElementType.HYDRO], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[1], 0)  # 第一个E技能
        self.check_health(1, [90, 10, 10])
        self.check_elemental_application(1, [[ElementType.HYDRO], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[1], 0)  # 第二个E技能，如果没有，则重复释放
        self.check_health(1, [89, 10, 10])
        self.check_elemental_application(1, [[ElementType.HYDRO], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[2], 0)  # Q技能
        self.check_health(1, [85, 10, 10])
        self.check_elemental_application(1, [[ElementType.HYDRO], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        # 用例执行 回合2:我方空过，对方行动 （承伤测试）
        self.game.active_player_index = 1
        self.run_actions_for_player(player1_init_actions, 1)
        # 对方A
        self.run_actions_for_player(skill_action_list[0], 1)
        self.assertEqual(self.game.players[0].character_list[0].health_point, 9)
        self.assertEqual(self.game.players[0].character_list[0].elemental_application, [])
        # 对方A
        self.run_actions_for_player(skill_action_list[0], 1)
        self.assertEqual(self.game.players[0].character_list[0].health_point, 7)
        self.assertEqual(self.game.players[0].character_list[0].elemental_application, [])

        # 回合1节末伤害检测
        self.check_health(1, [84, 10, 10])
        self.check_elemental_application(1, [[ElementType.HYDRO], [], []])

    def check_health(self, player, health):
        for i in range(len(health)):
            self.assertEqual(self.game.players[player].character_list[i].health_point, health[i])

    def check_elemental_application(self, player, element):
        for i in range(len(element)):
            self.assertEqual(self.game.players[player].character_list[i].elemental_application, element[i])


if __name__ == '__main__':
    unittest.main()
