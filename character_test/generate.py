from genius_invocation.game.game import GeniusGame
from genius_invocation.card.character.import_head import *
import re, os

template_file = "Character_Unit_Test/test_solo_shenhe.py"

character_dir = "./"
for character_file in os.listdir(character_dir):
    if character_file.startswith("gen"):
        continue
    if character_file.startswith("test_solo_Yae"):
        continue
    if character_file.startswith("test_solo_Venti"):
        continue
    character_name = character_file.split(".")[0].split("_")[-1]
    print(character_name)
    file_name = "test_solo_" + character_name + ".py"
    player0_deck = {
        'character': [character_name],
        'action_card': ['Thunder_and_Eternity'] * 30
    }
    game = GeniusGame(
        player0_deck=player0_deck,
        player1_deck=player0_deck)
    character = game.players[0].character_list[0]
    a_info = {}
    e_info = {}
    e2_info = {}
    q_info = {}
    element = character.element
    for skill in character.skills:
        if skill.type == SkillType.NORMAL_ATTACK:
            a_info["damage_type"] = skill.damage_type
            a_info["main_damage"] = skill.main_damage
            a_info["piercing_damage"] = skill.piercing_damage
            a_info["cost"] = 0
            for cost in skill.cost:
                a_info["cost"] = a_info["cost"] + cost["cost_num"]
        if skill.type == SkillType.ELEMENTAL_SKILL:
            if len(e_info.keys()) == 0:
                e_info["damage_type"] = skill.damage_type
                e_info["main_damage"] = skill.main_damage
                e_info["piercing_damage"] = skill.piercing_damage
                e_info["cost"] = 0
                for cost in skill.cost:
                    e_info["cost"] = e_info["cost"] + cost["cost_num"]
            else:
                e2_info["damage_type"] = skill.damage_type
                e2_info["main_damage"] = skill.main_damage
                e2_info["piercing_damage"] = skill.piercing_damage
                e2_info["cost"] = 0
                for cost in skill.cost:
                    e2_info["cost"] = e2_info["cost"] + cost["cost_num"]
        if skill.type == SkillType.ELEMENTAL_BURST:
            q_info["damage_type"] = skill.damage_type
            q_info["main_damage"] = skill.main_damage
            q_info["piercing_damage"] = skill.piercing_damage
            q_info["cost"] = 0
            for cost in skill.cost:
                q_info["cost"] = q_info["cost"] + cost["cost_num"]
    print(character_name)
    print(a_info)
    print(e_info)
    print(e2_info)
    print(q_info)
    health = [100, 10, 10]
    health1 = [health[0] - a_info["main_damage"], health[1] - a_info["piercing_damage"],
               health[2] - a_info["piercing_damage"]]
    health2 = [health1[0] - e_info["main_damage"], health1[1] - e_info["piercing_damage"],
               health1[2] - e_info["piercing_damage"]]
    health3 = []
    if len(e2_info.keys()) > 0:
        health3 = [health2[0] - e2_info["main_damage"], health2[1] - e2_info["piercing_damage"],
                   health2[2] - e2_info["piercing_damage"]]
    else:
        health3 = [health2[0] - e_info["main_damage"], health2[1] - e_info["piercing_damage"],
                   health2[2] - e_info["piercing_damage"]]
    health4 = [health3[0] - q_info["main_damage"], health3[1] - q_info["piercing_damage"],
               health3[2] - q_info["piercing_damage"]]
    health5 = [health4[0] - a_info["main_damage"], health4[1] - a_info["piercing_damage"],
               health4[2] - a_info["piercing_damage"]]
    health6 = [health5[0] - e_info["main_damage"], health5[1] - e_info["piercing_damage"],
               health5[2] - e_info["piercing_damage"]]
    health7 = []
    if len(e2_info.keys()) > 0:
        health7 = [health6[0] - e2_info["main_damage"], health6[1] - e2_info["piercing_damage"],
                   health6[2] - e2_info["piercing_damage"]]
    else:
        health7 = [health6[0] - e_info["main_damage"], health6[1] - e_info["piercing_damage"],
                   health6[2] - e_info["piercing_damage"]]
    health8 = [health7[0] - q_info["main_damage"], health7[1] - q_info["piercing_damage"],
               health7[2] - q_info["piercing_damage"]]

    with open(template_file, 'r', encoding='utf-8') as f:
        new_data = ""
        for line in f.readlines():
            # 设置类名
            if re.search("class TestShenhe\(TestBase, unittest.TestCase\):", line) is not None:
                line = line.replace(line, "class Test%s(TestBase, unittest.TestCase):\n" % character_name)
            if re.search("'character': \['Shenhe'],", line) is not None:
                line = line.replace(line, "        'character': ['%s'],\n" % character_name)
            # 如果有两个e技能的场合
            if len(e2_info.keys()) > 0:
                if e2_info["cost"] == 3:
                    if re.search("\[Action\(12, 0, \[0, 1, 2]\)]", line) is not None:
                        line = line.replace(line, "            [Action(12, 0, [0, 1, 2])],\n            [Action(13, 0, [0, 1, 2])]\n")
                if e2_info["cost"] == 5:
                    if re.search("\[Action\(12, 0, \[0, 1, 2]\)]", line) is not None:
                        line = line.replace(line, "            [Action(12, 0, [0, 1, 2, 3, 4])],\n            [Action(13, 0, [0, 1, 2])]\n")
                if re.search("# 第二个E技能，如果没有，则重复释放", line) is not None:
                    line = line.replace(line, "        self.run_actions_for_player(skill_action_list[2], 0)\n")
                if re.search("# Q技能", line) is not None:
                    line = line.replace(line, "        self.run_actions_for_player(skill_action_list[3], 0)\n")
            if re.search("# health1", line) is not None:
                line = line.replace(line, "        self.check_health(1, %s)\n" % health1)
            if re.search("# health2", line) is not None:
                line = line.replace(line, "        self.check_health(1, %s)\n" % health2)
            if re.search("# health3", line) is not None:
                line = line.replace(line, "        self.check_health(1, %s)\n" % health3)
            if re.search("# health4", line) is not None:
                line = line.replace(line, "        self.check_health(1, %s)\n" % health4)
            if re.search("# health5", line) is not None:
                line = line.replace(line, "        self.check_health(1, %s)\n" % health5)
            if re.search("# health6", line) is not None:
                line = line.replace(line, "        self.check_health(1, %s)\n" % health6)
            if re.search("# health7", line) is not None:
                line = line.replace(line, "        self.check_health(1, %s)\n" % health7)
            if re.search("# health8", line) is not None:
                line = line.replace(line, "        self.check_health(1, %s)\n" % health8)
            if re.search("self.check_elemental_application\(1, \[\[ElementType.CRYO], \[], \[]]\)", line) is not None:
                if element in [ElementType.GEO, ElementType.ANEMO]:
                    line = line.replace(line, "        self.check_elemental_application(1, [[], [], []])\n")
                else:
                    line = line.replace(line, "        self.check_elemental_application(1, [[%s], [], []])\n" % element)
            new_data += line
    with open(file_name, 'w', encoding='utf-8') as f:
        # pass
        f.write(new_data)
