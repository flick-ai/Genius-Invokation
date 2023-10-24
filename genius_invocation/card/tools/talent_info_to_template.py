import re, os
from genius_invocation.utils import *


en_json_file = "card_info_ambr_en.json"
cn_json_file = "card_info_ambr_cn.json"
template_file = "talent_template.txt"
target_file = "../action/equipment/talent/talents"

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
        if "GCG_TAG_TALENT" not in card_infos[info]["tags"].keys():
            continue
        id = card_infos[info]['id']
        name = card_infos[info]['name']
        name_strip = name.replace(":", "").replace(" ", "").replace(",","").replace("'","").replace("-","")
        cn_name = card_infos_cn[info]['name']
        if "GCG_TAG_SLOWLY" in card_infos[info]["tags"].keys():
            is_action = True
        else:
            is_action = False
        character = card_infos[info]['icon'].split("_")[-1]
        
        cost_power = 0
        cost = []
        props = card_infos[info]['props']
        for prop in props.keys():
            if prop.startswith("GCG_COST_ENERGY"):
                cost_power = props[prop]
            if prop.startswith("GCG_COST_DICE_DENDRO"):
                cost.append({'cost_num':props[prop], 'cost_type':CostType.DENDRO.value})
            if prop.startswith("GCG_COST_DICE_CRYO"):
                cost.append({'cost_num':props[prop], 'cost_type':CostType.CRYO.value})
            if prop.startswith("GCG_COST_DICE_ELECTRO"):
                cost.append({'cost_num':props[prop], 'cost_type':CostType.ELECTRO.value})
            if prop.startswith("GCG_COST_DICE_GEO"):
                cost.append({'cost_num':props[prop], 'cost_type':CostType.GEO.value})
            if prop.startswith("GCG_COST_DICE_ANEMO"):
                cost.append({'cost_num':props[prop], 'cost_type':CostType.ANEMO.value})
            if prop.startswith("GCG_COST_DICE_HYDRO"):
                cost.append({'cost_num':props[prop], 'cost_type':CostType.HYDRO.value})
            if prop.startswith("GCG_COST_DICE_PYRO"):
                cost.append({'cost_num':props[prop], 'cost_type':CostType.PYRO.value})
            if prop.startswith("GCG_COST_DICE_VOID"):
                cost.append({'cost_num':props[prop], 'cost_type':CostType.BLACK.value})   

        with open(template_file) as t:
            file_data = ""
            for line in t:
                if re.search("class \(TalentCard\):", line) is not None:
                    line = line.replace(line, "class %s(Character):\n" % name_strip)
                if re.search("id: int =", line) is not None:
                    line = line.replace(line, "    id: int = %s\n" % id)
                if re.search("name: str =", line) is not None:
                    line = line.replace(line, "    name: str = \"%s\"\n" % name)
                if re.search("name_ch: str =", line) is not None:
                    line = line.replace(line, "    name_ch = \"%s\"\n" % cn_name)
                if re.search("is_action: bool =", line) is not None:
                    line = line.replace(line, "    is_action = %s\n" % is_action)
                if re.search("cost =", line) is not None:
                    print(cost)
                    line = line.replace(line, "    cost = %s\n" % cost)
                if re.search("cost_power: int =", line) is not None:
                    line = line.replace(line, "    cost_power = %s\n" % cost_power)
                if re.search("character =", line) is not None:
                    line = line.replace(line, "    character = %s\n" % character)
                file_data += line

            # print(file_data)
            with open(os.path.join(target_file, '%s.py' % name_strip), 'w', encoding='utf-8') as file:
                file.write(file_data)
            # break
