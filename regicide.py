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
        command = command.upper()
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

class Player:
    def __init__(self, name=None, hand_limit=7):
        self.hand = []
        if name:
            self.name = name
        self.hand_limit = hand_limit

    def __str__(self):
        return f'{self.name}\n{self.show_hand()}'

    def draw_from_deck(self, deck, number=1)->bool:
        """Draws a specified number of cards from the deck and adds them to the player's hand.
        If the player doesn't draw number cards, due to hand limit or empty deck, returns False."""
        for _ in range(number):
            if len(self.hand) >= self.hand_limit:
                print(f'{self.name} is at hand limit of {self.hand_limit}')
                return False
            card = deck.draw_card()
            if card:
                self.hand.append(card)
                print(f"{self.name} has drawn: {card}")
            else:
                print("No more cards in the deck.")
                return False
            
        return True

    def show_hand(self, sorting=None)->str:
        self.hand = sorted(self.hand)

        if self.hand:
            return "Hand: " + ", ".join(str(card) for card in self.hand)
        else:
            return "Hand is empty."

    def has_card(self, command):
        """Checks if the player has a card that matches the command."""
        return any(card.check_card_command(command) for card in self.hand)

    def parse_and_check_command(self, command:str)->list[str]:
        """Takes a command str and verifies if it is formatted correctly.
        Verifies the command is for cards in the player's hand.
        Verifies the command follows multicard rules.
        """
        command = command.lower()
        command = command.replace('hearts', 'h').replace('diamonds', 'd').replace('clubs', 'c').replace('spades', 's')
        command = command.replace(' ', '').replace(',', '').replace('.', '').replace('of', '')
        cmd_list = []
        while len(command) > 0:
            if command.startswith('10'):
                cmd_list.append(command[:3])
                command = command[3:]
            else:
                cmd_list.append(command[:2])
                command = command[2:]

        # check if card(s) are in hand
        missing_cmd = None
        assert all(self.has_card(missing_cmd:=cmd) for cmd in cmd_list
                   ), f"Invalid command: {missing_cmd}. Incorrect format or card is unavailable."

        # TODO: check if multicard rules are followed
        # TODO: invert logic of multicard checks
        if len(cmd_list) == 1:
            pass
        elif len(cmd_list) == 2 and (has_ace:= any(cmd[0] == 'a' for cmd in cmd_list)):
            pass
        elif sum([card.value for card in cards]) <= 10 and len(set(card.value for card in cards)) == 1:
            pass
        else:
            raise ValueError("Invalid command: Multicard rules not followed.")
            
        return cmd_list
        
    def play_cards(self, commands)->list[Card]:
        """Returns list of cards specified in the commands.
        Removes the cards from the player's hand."""
        cards = []
        for command in commands:
            for card in self.hand:
                if card.check_card_command(command):
                    cards.append(card)
                    self.hand.remove(card)
                    break

        return cards

class RegicideGame:
    def __init__(self, player_names=['a','b']):
        self.turn_number = 1
        self.deck = Deck(deck_type='Tavern', shuffle=True)
        self.players = [Player(name=n) for n in player_names]
        self.active_player_index = 0
        self.active_player = self.players[self.active_player_index]
        self.enemies = Deck(deck_type='Castle')
        self.discard = Deck(deck_type='Empty')
        self.play_area = Deck(deck_type='Empty')
        self.running = True
        self.is_player_turn = True
        self.game_result = None
        self.setup_game()

    def setup_game(self):
        # Draw initial hand
        
        for player in self.players:
            player.draw_from_deck(self.deck, 7)
        
        # Start with the first enemy
        self.next_enemy()
    
    def get_enemy_health(self, value):
        return {'J': 20, 'Q': 30, 'K': 40}[value]

    def refill_tavern(self, number):
        """Shuffle discard then add specified number of cards from the discard to the bottom of the tavern deck."""
        print(f"\nRefilling the tavern with {number} cards.")
        
        self.discard.shuffle()
        
        for _ in range(number):
            if self.discard.cards:
                card = self.discard.draw_card()
                self.deck.add_card(card)
            else:
                print("No more cards in the discard pile.")
                break

        print(f"There are {len(self.discard)} cards in the discard pile.")
        print(f"There are {len(self.deck)} cards in the tavern deck.")
        
    def deal_to_players(self, number):
        """Deals a specified number of cards, cycling through the recieving player."""
        print(f"\nDealing {number} cards to players.")
        
        player_index = self.active_player_index
        for _ in range(number):
            self.players[player_index].draw_from_deck(self.deck)
            player_index = (player_index + 1) % len(self.players)

    def attack_enemy(self, cards:list[Card]):
        """Takes a list of cards, deals damage to enemy and applies suit effects."""
        assert self.current_enemy, "No enemy to attack!"

        cards_value = sum(card.get_card_attack() for card in cards)

        # apply suit effect clubs
        double_damage = (
            self.current_enemy.suit != 'Clubs' and
            any(card.suit == 'Clubs' for card in cards)
        )
        # assign damage
        total_damage = cards_value * (2 if double_damage else 1)
        print(f"\nYou played {', '.join(str(card) for card in cards)} for {total_damage} damage.")
        
        self.current_enemy.health -= total_damage

        # apply suit effect spades
        reduce_attack = (
            self.current_enemy.suit != 'Spades' and
            any(card.suit == 'Spades' for card in cards)
        )
        if reduce_attack:
            self.current_enemy.attack -= cards_value
            self.current_enemy.attack = 0 if self.current_enemy.attack < 0 else self.current_enemy.attack
            print(f"Enemy attack has been reduced by {cards_value}." )
            print(f"Enemy attack: {self.current_enemy.attack}")
            
        
        # apply suit effect hearts
        # important to apply hearts before diamonds
        refill_tavern = (
            self.current_enemy.suit != 'Hearts' and
            any(card.suit == 'Hearts' for card in cards)
        )
        if refill_tavern:
            self.refill_tavern(cards_value)
        
        # apply suit effect diamonds
        draw_cards = (
            self.current_enemy.suit != 'Diamonds' and
            any(card.suit == 'Diamonds' for card in cards)
        )
        if draw_cards:
            self.deal_to_players(cards_value)

    def print_game_state(self):
        print('\n')
        print(f" Turn {self.turn_number} ".center(20, '='))
        print(f"Current Enemy:")
        print(f"{self.current_enemy}".center(20))
        print(f"(Health: {self.current_enemy.health})".rjust(20))
        print(f"(Attack: {self.current_enemy.attack})".rjust(20))
        print()
        for player in self.players:
            print(f"{player.name} is holding {len(player.hand)}/{player.hand_limit} cards.")
        print()
        print(f"There are {len(self.deck)} cards in the tavern deck.")
        print(f"There are {len(self.discard)} cards in the discard pile.")

    def play_game(self):
        while self.running:
            self.print_game_state()
            self.player_turn()
            # check_enemy_defeated also checks for victory condition
            player_again = self.check_enemy_defeated()
            if self.running and not player_again:
                self.enemy_turn()
                self.turn_number += 1
                self.next_player()
            
        self.game_end()

    def game_end(self):
        if self.game_result == 'Win':
            print("You won the game!")
        else:
            print("You lost the game.")
        
        print("Thanks for playing!")

    def player_turn(self):
        print()
        print(f'It is {self.active_player.name}\'s turn')
        print(self.active_player.show_hand())

        valid_play = False
        while not valid_play:
            command = input("\ntype card(s) to play them, 'yield' to not attack, or 'quit' to quit: ").lower()
            print("\n")
            
            if command == 'quit':
                print("Thanks for playing!")
                self.running = False
                return
                
            elif command == 'yield':
                print("You chose not to attack this turn.")
                self.is_player_turn = False
                valid_play = True

            else:
                cmd_list = None
                try:
                    cmd_list = self.active_player.parse_and_check_command(command)
                except ValueError as e:
                    print(e)

                if cmd_list:
                    played_cards = self.active_player.play_cards(cmd_list)
                    self.play_area.add_card(played_cards)
                    self.attack_enemy(played_cards)
                    
                    self.is_player_turn = False
                    valid_play = True

    def next_player(self):
        self.active_player_index = (self.active_player_index + 1) % len(self.players)
        self.active_player = self.players[self.active_player_index]

    def enemy_turn(self):
        """On enemy turn, active player must discard cards to withstand enemy attack."""
        print(f"\nIt is {self.current_enemy}'s turn.")
        print(f"{self.active_player.name} must discard cards to withstand {self.current_enemy.attack} damage.")

        print(self.active_player.show_hand())

        valid_play = False
        while not valid_play:
            command = input("\ntype card(s) to play them").lower()

            cmd_list = None
            try:
                cmd_list = self.active_player.parse_and_check_command(command)
            except ValueError as e:
                print(e)

            # TODO: Implement defense turn logic

        
        
        self.is_player_turn = True

    def check_enemy_defeated(self):
        """Checks if the current enemy has been defeated.
        Updates self.current_enemy, if all enemies are defeated, sets self.running to False and self.game_result to 'Win'.
        If so, it returns True to allow the player to play again.
        If not, it returns False to end the player's turn."""
        if self.current_enemy.health <= 0:
            print(f"You defeated {self.current_enemy}!")

            if self.current_enemy.health == 0:
                print("Exact damage! Defeated Enemy added to the top of Tavern Deck")
                self.deck.add_card_on_top(self.current_enemy)
            else:
                print("Defeated enemy will go to the discard pile!")
                self.discard.add_card(self.current_enemy)

            self.next_enemy()
            return True
        else:
            print(f"{self.current_enemy} has {self.current_enemy.health} health remaining.")
            return False

    def next_enemy(self):
        """Draws a new enemy card from the deck.
        Moves all cards from the play area to the discard pile.
        If there are no more enemies, self.running = False and self.game_result = 'Win'."""
        if self.enemies:
            self.current_enemy = self.enemies.draw_card()
            print(f"\nNew enemy: {self.current_enemy} \n(Health: {self.current_enemy.health})\n(Attack: {self.current_enemy.attack})")
        else:
            print("Congratulations! You've defeated all enemies!")
            self.running = False
            self.game_result = 'Win'
            self.current_enemy = None


if __name__ == "__main__":
    game = RegicideGame(player_names=['Alice','Bob'])
    game.play_game()