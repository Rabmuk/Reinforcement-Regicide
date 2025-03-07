import random

class Card_Commands:
    int_to_cmd = ['yield_', 'ac', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', 'jc', 'qc', 'kc', 'ad', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', 'jd', 'qd', 'kd', 'ah', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', 'jh', 'qh', 'kh', 'as', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', 'js', 'qs', 'ks', 'ac2c', 'ac3c', 'ac4c', 'ac5c', 'ac6c', 'ac7c', 'ac8c', 'ac9c', 'ac10c', 'acjc', 'acqc', 'ackc', 'acad', 'ac2d', 'ac3d', 'ac4d', 'ac5d', 'ac6d', 'ac7d', 'ac8d', 'ac9d', 'ac10d', 'acjd', 'acqd', 'ackd', 'acah', 'ac2h', 'ac3h', 'ac4h', 'ac5h', 'ac6h', 'ac7h', 'ac8h', 'ac9h', 'ac10h', 'acjh', 'acqh', 'ackh', 'acas', 'ac2s', 'ac3s', 'ac4s', 'ac5s', 'ac6s', 'ac7s', 'ac8s', 'ac9s', 'ac10s', 'acjs', 'acqs', 'acks', 'ad2c', 'ad3c', 'ad4c', 'ad5c', 'ad6c', 'ad7c', 'ad8c', 'ad9c', 'ad10c', 'adjc', 'adqc', 'adkc', 'ad2d', 'ad3d', 'ad4d', 'ad5d', 'ad6d', 'ad7d', 'ad8d', 'ad9d', 'ad10d', 'adjd', 'adqd', 'adkd', 'adah', 'ad2h', 'ad3h', 'ad4h', 'ad5h', 'ad6h', 'ad7h', 'ad8h', 'ad9h', 'ad10h', 'adjh', 'adqh', 'adkh', 'adas', 'ad2s', 'ad3s', 'ad4s', 'ad5s', 'ad6s', 'ad7s', 'ad8s', 'ad9s', 'ad10s', 'adjs', 'adqs', 'adks', 'ah2c', 'ah3c', 'ah4c', 'ah5c', 'ah6c', 'ah7c', 'ah8c', 'ah9c', 'ah10c', 'ahjc', 'ahqc', 'ahkc', 'ah2d', 'ah3d', 'ah4d', 'ah5d', 'ah6d', 'ah7d', 'ah8d', 'ah9d', 'ah10d', 'ahjd', 'ahqd', 'ahkd', 'ah2h', 'ah3h', 'ah4h', 'ah5h', 'ah6h', 'ah7h', 'ah8h', 'ah9h', 'ah10h', 'ahjh', 'ahqh', 'ahkh', 'ahas', 'ah2s', 'ah3s', 'ah4s', 'ah5s', 'ah6s', 'ah7s', 'ah8s', 'ah9s', 'ah10s', 'ahjs', 'ahqs', 'ahks', 'as2c', 'as3c', 'as4c', 'as5c', 'as6c', 'as7c', 'as8c', 'as9c', 'as10c', 'asjc', 'asqc', 'askc', 'as2d', 'as3d', 'as4d', 'as5d', 'as6d', 'as7d', 'as8d', 'as9d', 'as10d', 'asjd', 'asqd', 'askd', 'as2h', 'as3h', 'as4h', 'as5h', 'as6h', 'as7h', 'as8h', 'as9h', 'as10h', 'asjh', 'asqh', 'askh', 'as2s', 'as3s', 'as4s', 'as5s', 'as6s', 'as7s', 'as8s', 'as9s', 'as10s', 'asjs', 'asqs', 'asks', '2c2d', '2c2h', '2c2s', '2d2h', '2d2s', '2h2s', '2c2d2h', '2c2d2s', '2c2h2s', '2d2h2s', '2c2d2h2s', '3c3d', '3c3h', '3c3s', '3d3h', '3d3s', '3h3s', '3c3d3h', '3c3d3s', '3c3h3s', '3d3h3s', '4c4d', '4c4h', '4c4s', '4d4h', '4d4s', '4h4s', '5c5d', '5c5h', '5c5s', '5d5h', '5d5s', '5h5s']
    cmd_to_int = {cmd:index for index, cmd in enumerate(int_to_cmd)}
        

class Card:
    def __init__(self, suit:str, value):
        self.suit = suit.title()
        self.value = value.upper()
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
        
    @staticmethod
    def get_cmd_attack(command):
        """assumes command is properly formatted"""
        cmd_value = command[:-1].lower()
        match cmd_value:
            case 'j':
                return 10
            case 'q':
                return 15
            case 'k':
                return 20
            case 'a':
                return 1
            case _:
                return int(cmd_value)
        
    def check_card_command(self, command:str)->bool:
        command = command.upper()
        if not command.startswith(self.value):
            return False
        command = command.strip(self.value)
        if len(command) == 1 and command.lower() == self.suit[0].lower():
            return True
        if command.lower() == self.suit.lower():
            return True

        return False
    
    def get_cmd(self):
        return (str(self.value) + self.suit[0]).lower()
    
    def get_int_value(self):
        return Card_Commands.cmd_to_int[self.get_cmd()]

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

    def __len__(self):
        return len(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None
    
    def add_card(self, card:Card | list[Card]):
        """Adds a card or list of cards to the deck."""
        if isinstance(card, list):
            for c in card:
                self.cards.append(c)
        elif isinstance(card, Card):
            self.cards.append(card)

    def add_card_on_top(self, card):
        self.cards.insert(0, card) 

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

