from card.players import CHARACTER_STATES

class GameState:
    def __init__(self):
        self.character_state: CHARACTER_STATES
        self.card: CardState
        self.support_region: SupportState