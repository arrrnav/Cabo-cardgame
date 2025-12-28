import random

class CardGame:
    def __init__(self):
        self.players = []  # List of dicts: {'id': socket_id, 'name': name, 'hand': []}
        self.deck = self._generate_deck()
        self.started = False
        self.turn_index = 0

    def _generate_deck(self):
        suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [{'suit': s, 'rank': r} for s in suits for r in ranks]
        random.shuffle(deck)
        return deck

    def add_player(self, player_id, name):
        if len(self.players) < 6 and not self.started:
            self.players.append({'id': player_id, 'name': name, 'hand': []})
            return True
        return False

    def remove_player(self, player_id):
        self.players = [p for p in self.players if p['id'] != player_id]

    def deal_cards(self, count=5):
        self.started = True
        for _ in range(count):
            for player in self.players:
                if self.deck:
                    player['hand'].append(self.deck.pop())

    def get_state(self):
        return {
            "player_count": len(self.players),
            "players": [{"name": p['name'], "card_count": len(p['hand'])} for p in self.players],
            "started": self.started,
            "current_turn": self.players[self.turn_index]['name'] if self.started else None
        }