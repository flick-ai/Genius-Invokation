import genius_invocation.card.action as action
import genius_invocation.card.character.characters as chars
import inspect
import js
from pyodide import create_proxy, to_js

def get_card():
    available_character_name = ['Arataki_Itto', 'Candace', 'Cyno', 'Dehya', "ElectroHypostasis", "Eula", 
                            "Fatui_Pyro_Agent", "Fischl", "Ganyu", "Jadeplume_Terrorshroom", "Keqing", 
                            "Mona", "Nahida", "Ningguang", "Noelle", "Qiqi", "Raiden_Shogun",
                            "Rhodeia_of_Loch", "Shenhe", "Tartaglia", "Wanderer", "Xingqiu", "Yae_Miko",
                            "Yoimiya"]
    available_character = []
    for name in available_character_name:
        available_character.append((name, eval("chars."+name).name, eval("chars."+name).name_ch))

    js_available_character = {available_character[i][2]: available_character[i][0] for i in range(len(available_character))}
    js.modify_object(create_proxy(js_available_character))
    # print(available_character)
    # available_card = []
    # ignore = [action.ActionCard, action.EquipmentCard, action.WeaponCard, action.TalentCard, action.ArtifactCard, action.SupportCard, action.FoodCard]
    # for name, obj in inspect.getmembers(action):
    #     if inspect.isclass(obj) and obj not in ignore:
    #         available_card.append((name, obj.name, obj.name_ch))




# print(available_card)