import re, os
from genius_invocation.card.character.import_head import *


en_json_file = "card_info_ambr_en.json"
cn_json_file = "card_info_ambr_cn.json"
template_file = "card_template.txt"
target_file = "../character/characters_to_be_completed"

with open(en_json_file) as en, open(cn_json_file, encoding='utf-8') as cn:
    card_data = json.load(en)
    card_data_cn = json.load(cn)
    card_infos = card_data['data']['items']
    card_infos_cn = card_data_cn['data']['items']
    for info in card_infos.keys():
        if card_infos[info]["type"] != "characterCard":
            continue
        id = card_infos[info]['id']
        name = card_infos[info]['name']
        name_strip = name.replace(":", "").replace(" ", "")
        cn_name = card_infos_cn[info]['name']

        tags = card_infos[info]['tags']
        for tag in tags.keys():
            if tag.startswith("GCG_TAG_ELEMENT"):
                element_type = tags[tag]
            if tag.startswith("GCG_TAG_WEAPON"):
                weapon = tags[tag]
            if tag.startswith("GCG_TAG_CAMP"):
                country = tags[tag]
            if tag.startswith("GCG_TAG_NATION"):
                country = tags[tag]

        props = card_infos[info]['props']
        hp = props['GCG_PROP_HP']
        energy = props['GCG_PROP_ENERGY']
        match weapon:
            case 'Sword':
                weapon = WeaponType.SWORD
            case 'Catalyst':
                weapon = WeaponType.CATALYST
            case 'Claymore':
                weapon = WeaponType.CLAYMORE
            case 'Bow':
                weapon = WeaponType.BOW
            case 'Polearm':
                weapon = WeaponType.POLEARM
            case 'Other Weapons':
                weapon = WeaponType.OTHER
        match country:
            case 'Mondstadt':
                country = CountryType.MONDSTADT
            case 'Liyue':
                country = CountryType.LIYUE
            case 'Inazuma':
                country = CountryType.INAZUMA
            case 'Sumeru':
                country = CountryType.SUNERU
            case 'Fontaine':
                country = CountryType.FONTAINE
            case 'Natlan':
                country = CountryType.NATLAN
            case 'Fatui':
                country = CountryType.FATUI
            case 'Hilichurl':
                country = CountryType.HILICHURL
            case 'Monster':
                country = CountryType.MONSTER
            case _:
                country = CountryType.OTHER
        match element_type:
            case 'Cryo':
                element_type = ElementType.CRYO
            case 'Hydro':
                element_type = ElementType.HYDRO
            case 'Pyro':
                element_type = ElementType.PYRO
            case 'Electro':
                element_type = ElementType.ELECTRO
            case 'Anemo':
                element_type = ElementType.ANEMO
            case 'Geo':
                element_type = ElementType.GEO
            case 'Dendro':
                element_type = ElementType.DENDRO

        with open(template_file) as t:
            file_data = ""
            for line in t:
                if re.search("class \(Character\):", line) is not None:
                    line = line.replace(line, "class %s(Character):\n" % name_strip)
                if re.search("id: int =", line) is not None:
                    line = line.replace(line, "    id: int = %s\n" % id)
                if re.search("name: str =", line) is not None:
                    line = line.replace(line, "    name: str = \"%s\"\n" % name)
                if re.search("name_ch =", line) is not None:
                    line = line.replace(line, "    name_ch = \"%s\"\n" % cn_name)
                if re.search("init_health_point: int =", line) is not None:
                    line = line.replace(line, "    init_health_point: int = %s\n" % hp)
                if re.search("max_health_point: int =", line) is not None:
                    line = line.replace(line, "    max_health_point: int = %s\n" % hp)
                if re.search("max_power: int =", line) is not None:
                    line = line.replace(line, "    max_power: int = %s\n" % energy)
                if re.search("weapon_type: WeaponType =", line) is not None:
                    line = line.replace(line, "    weapon_type: WeaponType = %s\n" % weapon)
                if re.search("country: CountryType =", line) is not None:
                    line = line.replace(line, "    country: CountryType = %s\n" % country)
                if re.search("element: ElementType =", line) is not None:
                    line = line.replace(line, "    element: ElementType = %s\n" % element_type)
                file_data += line

            # print(file_data)
            with open(os.path.join(target_file, '%s.py' % name_strip), 'w', encoding='utf-8') as file:
                file.write(file_data)
            # break
