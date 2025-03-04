import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.health = self.get_card_health()
        self.attack = self.get_card_attack()

    def __str__(self):
        return f"{self.value} of {self.suit}"

    def __lt__(self, other, sort_type='suit'):
        # Define the order of suits
        suit_order = {'Spades': 0, 'Clubs': 1, 'Hearts': 2, 'Diamonds': 3}
        
        # Define the order of values
        value_order = {'K': 13, 'Q': 12, 'J': 11, '10': 10, '9': 9, '8': 8, 
                       '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'A': 1}

        if sort_type == 'suit':
            if self.suit != other.suit:
                return suit_order[self.suit] < suit_order[other.suit]

        return value_order[self.value] < value_order[other.value]
    
    def get_card_health(self)->int:
        if self.value == 'J':
            return 20
        elif self.value == 'Q':
            return 30
        elif self.value == 'K':
            return 40
        else:
            return 0
    
    def get_card_attack(self)->int:
        if self.value == 'J':
            return 10
        elif self.value == 'Q':
            return 15
        elif self.value == 'K':
            return 20
        elif self.value == 'A':
            return 1
        else:
            return int(self.value)
        
    def check_card_command(self, command:str)->bool:
        if not command.startswith(self.value):
            return False
        command = command.strip(self.value)
        if len(command) == 1 and command.lower() == self.suit[0].lower():
            return True
        if command.lower() == self.suit.lower():
            return True

        return False

class Deck:
    def __init__(self, deck_type:str='Normal', shuffle:bool=True):
        """
        Create a deck of cards based on the specified type.

        Parameters:
        deck_type (str): The type of deck to create. Options are:
        - 'Normal': Standard 52-card deck.
        - 'Tavern': 40-card deck with values 2-10 and A.
        - 'Castle': 12-card deck with J, Q, K.  
        - 'Empty': An empty deck.
        """
        self.cards = []
        if deck_type == 'Normal':
            suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
            values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            self.cards = [Card(suit, value) for suit in suits for value in values]
        if deck_type == 'Tavern':
            suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
            values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
            self.cards = [Card(suit, value) for suit in suits for value in values]
        if deck_type == 'Castle':
            suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
            values = ['K', 'Q', 'J',]
            for value in values:
                random.shuffle(suits)
                for suit in suits:
                    self.cards.append(Card(suit, value))
            shuffle = False
        if deck_type == 'Empty':
            self.cards = []
        if shuffle:
            self.shuffle()

    def draw_card(self):
        return self.cards.pop() if self.cards else None
    
    def add_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

class Player:
    def __init__(self, name=None, hand_limit=7):
        self.hand = []
        if name:
            self.name = name
        self.hand_limit = hand_limit

    def __str__(self):
        return f'{self.name}\n{self.show_hand()}'

    def draw_from_deck(self, deck, number=1):
        for _ in range(number):
            if len(self.hand) >= self.hand_limit:
                print(f'{self.name} is at hand limit of {self.hand_limit}')
                break
            card = deck.draw_card()
            if card:
                self.hand.append(card)
                print(f"{self.name} has drawn: {card}")
            else:
                print("No more cards in the deck.")

    def show_hand(self, sorting=None)->str:
        self.hand = sorted(self.hand)

        if self.hand:
            return "Hand: " + ", ".join(str(card) for card in self.hand)
        else:
            return "Hand is empty."

    def has_card(self, command):
        """Checks if the player has a card that matches the command."""
        return any(card.check_card_command(command) for card in self.hand)

    def parse_and_check_command(self, command):
        """Takes a str and verifies if it is formatted correctly and that this player has the required cards."""
        commands = []
        while len(command) > 0:
            if command.startswith('10'):
                commands.append(command[:3])
                command = command[3:]
            else:
                commands.append(command[:2])
                command = command[2:]
        if all(self.has_card(cmd) for cmd in commands):
            return commands
        else:
            return False

    def play_cards(self, command):
        pass

class RegicideGame:
    def __init__(self, player_names=['a','b']):
        self.turn = 0
        self.deck = Deck(deck_type='Tavern', shuffle=True)
        self.players = [Player(name=n) for n in player_names]
        self.active_player = self.players[0]
        self.enemies = Deck(deck_type='Castle')
        self.discard = Deck(deck_type='Empty')
        self.running = True
        self.is_player_turn = True
        self.setup_game()

    def setup_game(self):
        # Draw initial hand
        
        for player in self.players:
            player.draw_from_deck(self.deck, 7)
        
        # Start with the first enemy
        self.next_enemy()
    
    def next_enemy(self):
        if self.enemies:
            self.current_enemy = self.enemies.draw_card()
            print(f"\nNew enemy: {self.current_enemy} \n(Health: {self.current_enemy.health})\n(Attack: {self.current_enemy.attack})")
        else:
            print("Congratulations! You've defeated all enemies!")
            self.current_enemy = None

    def get_enemy_health(self, value):
        return {'J': 20, 'Q': 30, 'K': 40}[value]

    def check_valid_play(self, cards):
        if len(cards) == 1:
            return True
        elif len(cards) == 2 and (has_ace:= any(card.value == 'A' for card in cards)):
            return True          
        elif sum([card.value for card in cards]) <= 10 and len(set(card.value for card in cards)) == 1:
            return True
            
        return False

    def get_card_value(self, card):
        if card.value in ['J', 'Q', 'K']:
            return {'J': 10, 'Q': 15, 'K': 20}[card.value]
        elif card.value == 'A':
            return 1
        else:
            return int(card.value)

    def play_card(self, card_index):
        if not self.current_enemy:
            print("No enemy to attack!")
            return

        card = self.player.hand[card_index]
        damage = self.get_card_value(card)
        
        print(f"\nYou played {card} for {damage} damage.")
        self.current_enemy.health -= damage
        
        if self.current_enemy.health <= 0:
            print(f"You defeated {self.current_enemy}!")
            self.next_enemy()
        else:
            print(f"{self.current_enemy} has {self.current_enemy.health} health remaining.")

        self.player.hand.pop(card_index)

    def play_game(self):
        while self.running:
            while self.is_player_turn:
                print()
                print(f'It is {self.active_player.name}\'s turn')
                print(self.active_player.show_hand())
                command = input("\ntype card(s) to play them, 'yield' to not attack, or 'quit' to quit: ").lower()
                print("\n")
                
                if command == 'quit':
                    print("Thanks for playing!")
                    self.running = False
                    
                elif command == 'yield':
                    print("You chose not to attack this turn.")
                    self.enemy_attack()
                elif self.active_player.can_play(command):
                    cards = self.player.get_cards(command)
                else:
                    print("Invalid command.")
            while not self.is_player_turn:
                pass

if __name__ == "__main__":
    game = RegicideGame(player_names=['Alice','Bob'])
    game.play_game()