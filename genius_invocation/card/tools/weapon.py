import re, os
from genius_invocation.utils import *


en_json_file = "card_info_ambr_en.json"
cn_json_file = "card_info_ambr_cn.json"
template_file = "weapon_template.txt"
target_file = "../action/equipment/weapon/1"

with open(en_json_file) as en, open(cn_json_file, encoding='utf-8') as cn:
    card_data = json.load(en)
    card_data_cn = json.load(cn)
    card_infos = card_data['data']['items']
    card_infos_cn = card_data_cn['data']['items']
    for info in card_infos.keys():
        if card_infos[info]["type"] != "actionCard":
            continue
        if 'tags' not in card_infos[info].keys():
            continue
        if card_infos[info]["tags"] is None:
            continue
        if "GCG_TAG_WEAPON" not in card_infos[info]["tags"].keys():
            continue
        id = card_infos[info]['id']
        if id > 312015:
            continue
        name = card_infos[info]['name']
        name_strip = name.replace(":", "").replace(" ", "").replace(",","").replace("'","").replace("-","")
        cn_name = card_infos_cn[info]['name']
        
        weapon_type = None
        match list(card_infos[info]["tags"].keys())[1]:
            case "GCG_TAG_WEAPON_BOW":
                weapon_type = WeaponType.BOW
            case "GCG_TAG_WEAPON_CATALYST":
                weapon_type = WeaponType.CATALYST
            case "GCG_TAG_WEAPON_CLAYMORE":
                weapon_type = WeaponType.CLAYMORE
            case "GCG_TAG_WEAPON_POLE":
                weapon_type = WeaponType.POLEARM
            case "GCG_TAG_WEAPON_SWORD":
                weapon_type = WeaponType.SWORD

        cost_num = 0
        cost_type = None
        props = card_infos[info]['props']
        for prop in props.keys():
            if prop.startswith("GCG_COST_DICE_VOID"):
                cost_type = CostType.BLACK
            if prop.startswith("GCG_COST_DICE_SAME"):
                cost_type = CostType.WHITE
            cost_num = props[prop]

        with open(template_file) as t:
            file_data = ""
            for line in t:
                if re.search("class \(WeaponCard\)", line) is not None:
                    line = line.replace(line, "class %s(WeaponCard):\n" % name_strip)
                if re.search("id: int =", line) is not None:
                    line = line.replace(line, "    id: int = %s\n" % id)
                if re.search("name: str =", line) is not None:
                    line = line.replace(line, "    name: str = \"%s\"\n" % name)
                if re.search("name_ch =", line) is not None:
                    line = line.replace(line, "    name_ch = \"%s\"\n" % cn_name)
                if re.search("weapon_type: WeaponType = ", line) is not None:
                    line = line.replace(line, "    weapon_type: WeaponType = %s\n" % weapon_type)
                if re.search("cost_num: int = ", line) is not None:
                    line = line.replace(line, "    cost_num: int = %s\n" % cost_num)
                if re.search("class Weapon\(Weapon\)", line) is not None:
                    line = line.replace(line, "class %sWeapon(Weapon):\n" % name_strip)
                if re.search("cost_type: CostType = ", line) is not None:
                    line = line.replace(line, "    cost_type: CostType = %s\n" % cost_type)
                if re.search("self.equipment_entity = Weapon", line) is not None:
                    line = line.replace(line, "        self.equipment_entity = %sWeapon\n" % name_strip)
                file_data += line

            # print(file_data)
            with open(os.path.join(target_file, '%s.py' % name_strip), 'w', encoding='utf-8') as file:
                file.write(file_data)
            # break
