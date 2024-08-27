from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

def get_dict(game: 'GeniusGame'):
    message = {'game':{}, 1:{}, 0:{}}

    message['game']['round']: int = game.round
    message['game']['round_phase']: str = game.game_phase.value
    message['game']['active_player']: int = game.active_player_index
    message['game']['first_player']: int = game.first_player

    for idx in [0, 1]:
        player = game.players[idx]
        message[idx]["dice_zone"]: List[str] = [DiceType(dice).name for dice in player.dice_zone.show()] if player.dice_zone.num()>0 else []
        message[idx]["card_zone"]: int = player.card_zone.num() 
        message[idx]["hand_zone"]: List[str] = [card.name_ch for card in player.hand_zone.card]
        message[idx][ZoneType.SUMMON_ZONE]: List[List[str]] = [[] for i in range(MAX_SUMMON)]
        for i, summon in enumerate(player.summon_zone.space):
            message[idx][ZoneType.SUMMON_ZONE][i] = [summon.name_ch,  str(summon.show())]
        message[idx][ZoneType.SUPPORT_ZONE]: List[List[str]] = [[] for i in range(MAX_SUPPORT)]
        for i, support in enumerate(player.support_zone.space):
            message[idx][ZoneType.SUPPORT_ZONE][i] =  [support.name_ch,  str(support.show())]
        [[support.name_ch,  str(support.show())]for support in player.support_zone.space]
        message[idx][ZoneType.CHARACTER_ZONE]: List[List[str]] = []
        for character in player.character_list:
            m = [Elementals_to_str(character.elemental_application),
             character.name_ch,
             character.show(),
             str(character.power),
            ]
            if character.character_zone.weapon_card != None:
                m.append(character.character_zone.weapon_card.show())
            if character.character_zone.artifact_card != None:
                m.append(character.character_zone.artifact_card.show())
            if character.talent == True:
                m.append("Has Talent")
            for skill in character.skills:
                m.append(skill.name_ch)
            for status in character.character_zone.status_list:
                m.append(f"{status.name_ch}:{status.show()}")
            if character.is_active:
                m.append("Active")
                for status in player.team_combat_status.shield:
                    m.append(f"{status.name_ch}:{status.show()}")
                for status in player.team_combat_status.space:
                    m.append(f"{status.name_ch}:{status.show()}")
            message[idx][ZoneType.CHARACTER_ZONE].append(m)
    return message

def compare_dict(dict1, dict2):
    diff_zone = []
    for idx in [0,1]:
        for key in dict1[idx].keys():
            if key in [ZoneType.CHARACTER_ZONE, ZoneType.SUMMON_ZONE, ZoneType.SUPPORT_ZONE]:
                for i in range(len(dict1[idx][key])):
                    if dict1[idx][key][i] != dict2[idx][key][i]:
                        diff_zone.append((idx, key, i,))
    return diff_zone
  
            