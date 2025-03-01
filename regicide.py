import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

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
            values = ['J', 'Q', 'K',]
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
    def __init__(self):
        self.hand = []

    def draw_from_deck(self, deck, number=1):
        for _ in range(number):
            card = deck.draw_card()
            if card:
                self.hand.append(card)
                print(f"Drawn: {card}")
            else:
                print("No more cards in the deck.")

    def show_hand(self, sorting=None):
        self.hand = sorted(self.hand)

        if self.hand:
            print("Your hand:", ", ".join(str(card) for card in self.hand))
        else:
            print("Your hand is empty.")

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
    def __init__(self, player_count=2):
        self.turn = 0
        self.deck = Deck(deck_type='Tavern', shuffle=True)
        self.players = [Player() for _ in range(player_count)]
        self.current_player = 0
        self.enemies = Deck(deck_type='Castle')
        self.discard = Deck(deck_type='Empty')
        self.setup_game()

    def setup_game(self):
        # Draw initial hand
        self.player.draw_from_deck(self.deck, 7)
        
        # Start with the first enemy
        self.next_enemy()
    
    def next_enemy(self):
        if self.enemies:
            self.current_enemy = self.enemies.draw_card()
            self.current_enemy.health = self.get_enemy_health(self.current_enemy.value)
            self.current_enemy.attack = self.get_enemy_attack(self.current_enemy.value)
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
        while True:
            command = input("\ntype card(s) to play them, 'yield' to not attack, or 'quit' to quit: ").lower()
            print("\n")
            
            if command == 'quit':
                print("Thanks for playing!")
                break
            elif command == 'yield':
                print("You chose not to attack this turn.")
                self.enemy_attack()
            elif self.player.can_play(command):
                cards = self.player.get_cards(command)
            
            if command == 'p' or command == 'play':
                if not self.player.hand:
                    print("Your hand is empty. Draw a card first.")
                    continue
                
                while True:
                    try:
                        self.player.show_hand()
                        card_index = int(input(f"Which card do you want to play? (0-{len(self.player.hand)-1}): "))
                        print("\n \n")
                        if 0 <= card_index < len(self.player.hand):
                            self.play_card(card_index)
                            break
                        else:
                            print("Invalid card index. Try again.")
                    except ValueError:
                        print("Please enter a valid number.")

            else:
                print("Invalid command.")

if __name__ == "__main__":
    game = RegicideGame()
    game.play_game()