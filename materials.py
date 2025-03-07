import random

class Card_Commands:
    int_to_cmd = ['ac' ,'2c' ,'3c' ,'4c' ,'5c' ,'6c' ,'7c' ,'8c' ,'9c' ,'10c' ,'jc' ,'qc' ,'kc' ,'ad' ,'2d' ,'3d' ,'4d' ,'5d' ,'6d' ,'7d' ,'8d' ,'9d' ,'10d' ,'jd' ,'qd' ,'kd' ,'ah' ,'2h' ,'3h' ,'4h' ,'5h' ,'6h' ,'7h' ,'8h' ,'9h' ,'10h' ,'jh' ,'qh' ,'kh' ,'as' ,'2s' ,'3s' ,'4s' ,'5s' ,'6s' ,'7s' ,'8s' ,'9s' ,'10s' ,'js' ,'qs' ,'ks' ,'yeild_' ,]
    cmd_to_int = {cmd:index for index, cmd in enumerate(int_to_cmd)}

    @classmethod
    def int_list_to_cmd(cls, int_list:list[int]):
        cmd_list = [
            cls.int_to_cmd[i]
            for i in int_list
        ]
        return ','.join(cmd_list)
        

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

