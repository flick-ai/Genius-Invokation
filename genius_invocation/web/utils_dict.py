from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

def Elementals_to_str(elements: List[ElementType]):
    res = ""
    for element in elements:
        res += str(element.name)+ " "
    if res == "":
        res = "None"
    return res

def get_dict(game: 'GeniusGame'):
    message = {'game':{}, 1:{}, 0:{}}

    message['game']['round']: int = game.round
    message['game']['round_phase']: str = game.game_phase.name
    message['game']['active_player']: int = game.active_player_index
    message['game']['first_player']: int = game.first_player

    for idx in [0, 1]:
        player = game.players[idx]
        message[idx]["dice_zone"]: List[str] = [DiceType(dice).name for dice in player.dice_zone.show()] if player.dice_zone.num()>0 else []
        message[idx]["card_zone"]: int = player.card_zone.num() 
        message[idx]["hand_zone"]: List[str] = [card.name for card in player.hand_zone.card]
        message[idx]["summon_zone"]: List[List[str]] = [[summon.name,  str(summon.show())]for summon in player.summon_zone.space]
        message[idx]["support_zone"]: List[List[str]] = [[support.name,  str(support.show())]for support in player.support_zone.space]
        message[idx]["character_zone"] = [{}, {}, {}]
        for i, character in enumerate(player.character_list):
            message[idx]["character_zone"][i]['base'] = [Elementals_to_str(character.elemental_application).strip(),
             character.name,
             character.show(),
             str(character.power),
             character.is_active
            ]
            if character.character_zone.weapon_card != None:
                message[idx]["character_zone"][i]['weapon'] = character.character_zone.weapon_card.show()
            if character.character_zone.artifact_card != None:
                message[idx]["character_zone"][i]['artifact'] = character.character_zone.artifact_card.show()
            if character.talent == True:
                message[idx]["character_zone"][i]['talent'] = "Has Talent"
            message[idx]["character_zone"][i]['skills'] = [skill.name for skill in character.skills]
            message[idx]["character_zone"][i]['status'] = [f"{status.name}:{status.show()}" for status in character.character_zone.status_list]
            
            if character.is_active:
                message[idx]["character_zone"][i]['active'] = "Active"
                message[idx]["character_zone"][i]['shield'] = [f"{status.name}:{status.show()}" for status in player.team_combat_status.shield]
                message[idx]["character_zone"][i]['active_status'] = [f"{status.name}:{status.show()}" for status in player.team_combat_status.space]
            # message[idx]["character_zone"].append(m)
    return message
  
            