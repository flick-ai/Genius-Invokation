import genius_invocation.card.action as action
import genius_invocation.card.character.characters as chars
import inspect
import js

def get_card():
    available_character_name = ['Arataki_Itto', 'Candace', 'Cyno', 'Dehya', "ElectroHypostasis", 
                            "Fatui_Pyro_Agent", "Fischl", "Ganyu", "Jadeplume_Terrorshroom", "Keqing", 
                            "Mona", "Nahida", "Ningguang", "Noelle", "Qiqi",
                            "Rhodeia_of_Loch", "Shenhe", "Tartaglia", "Xingqiu", "Yae_Miko",
                            "Yoimiya"]
    available_character = []
    for name in available_character_name:
        available_character.append((name, eval("chars."+name).name, eval("chars."+name).name_ch))

    js.available_character = {available_character[i][2]: available_character[i][0] for i in range(len(available_character))}
    print(js.available_character)
    # print(available_character)
    available_card = []
    ignore = [action.ActionCard, action.EquipmentCard, action.WeaponCard, action.TalentCard, action.ArtifactCard, action.SupportCard, action.FoodCard]
    for name, obj in inspect.getmembers(action):
        if inspect.isclass(obj) and obj not in ignore:
            available_card.append((name, obj.name, obj.name_ch))




# print(available_card)