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
        message[idx]["hand_zone"]: List[str] = [card.name for card in player.hand_zone.card]
        message[idx]["summon_zone"]: List[List[str]] = [[summon.name,  str(summon.show())]for summon in player.summons_zone.space]
        message[idx]["support_zone"]: List[List[str]] = [[support.name,  str(support.show())]for support in player.support_zone.space]
        message[idx]["character_zone"]: List[List[str]] = []
        for character in player.character_list:
            m = [Elementals_to_str(character.elemental_application),
             character.name,
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
                m.append(skill.name)
            for status in character.character_zone.status_list:
                m.append(f"{status.name}:{status.show()}")
            if character.is_active:
                for status in player.team_combat_status.shield:
                    m.append(f"{status.name}:{status.show()}")
                for status in player.team_combat_status.space:
                    m.append(f"{status.name}:{status.show()}")
            message[idx]["character_zone"].append(m)
    return message
  
            