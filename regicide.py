from materials import Card, Deck, Card_Commands

class Player:
    def __init__(self, name:str=None, hand_limit:int=7):
        self.hand: list[Card] = []
        if name:
            self.name:str = name
        self.hand_limit:int = hand_limit

    def __str__(self):
        return f'{self.name}\n{self.show_hand()}'

    def draw_from_deck(self, deck:Deck, number:int=1)->bool:
        """Draws a specified number of cards from the deck and adds them to the player's hand.
        If the player doesn't draw number cards, due to hand limit or empty deck, returns False."""
        for _ in range(number):
            if len(self.hand) >= self.hand_limit:
                # print(f'{self.name} is at hand limit of {self.hand_limit}')
                return False
            card = deck.draw_card()
            if card:
                self.hand.append(card)
                # print(f"{self.name} has drawn: {card}")
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

    def count_cards_in_hand(self)->int:
        """
        Returns the len of self.hand
        """
        return len(self.hand)

    @staticmethod
    def parse_command(command:str)->list[str]:
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

        return cmd_list

    def has_card(self, command):
        """Checks if the player has a card that matches the command."""
        return any(card.check_card_command(command) for card in self.hand)

    def valid_cmd_list(self, cmd_list):
        return all(self.has_card(cmd) for cmd in cmd_list)

    def assert_valid_cmd_list(self, cmd_list):
        """
        Asserts that all commands in cmd_list match a card in Player's hand.
        """
        missing_cmd = None
        assert all(self.has_card(missing_cmd:=cmd) for cmd in cmd_list
                   ), f"Invalid command: {missing_cmd}. Incorrect format or card is unavailable."
        return True

    def validate_attack_command(self, command:str)->list[str]:
        """Takes a command str and parses it into a list of str.
        Asserts each command is for a card in the player's hand.
        Asserts the command follows attack multicard rules.
        """
        cmd_list = Player.parse_command(command)

        # check if card(s) are in hand
        self.assert_valid_cmd_list(cmd_list)

        valid_play = False
        # 1 card is always valid play
        if len(cmd_list) == 1:
            valid_play = True
        # 2 cards when 1 is ace is always valid
        elif len(cmd_list) == 2 and any(cmd[0] == 'a' for cmd in cmd_list):
            valid_play = True
        # all cards same value
        elif len(set(cmd[:-1] for cmd in cmd_list)) == 1:
            # must be 2 to 5, with total value less than 10
            if cmd_list[0][:-1] in ['2','3','4','5'] and len(cmd_list) * int(cmd_list[0][:-1]) <= 10:
                valid_play = True

        assert valid_play, ("Invalid command: Multicard rules not followed." + f"{cmd_list}")
            
        return cmd_list

    def validate_defend_command(self, command:str, incoming_damage:int)->list[str]:
        """Takes a command str and parses it into a list of str.
        Asserts each command is for a card in the player's hand.
        Asserts total value of commands is greater than incoming_damage.
        """
        cmd_list = Player.parse_command(command)

        # check if card(s) are in hand
        self.assert_valid_cmd_list(cmd_list)

        total_value = sum(Card.get_cmd_attack(cmd) for cmd in cmd_list)
        assert total_value >= incoming_damage, (f"{total_value} is not enough to block enemy attack of {incoming_damage}")

        return cmd_list

    def calc_max_defense(self)->int:
        """
        Sums total defense of all cards
        """
        return sum([card.attack for card in self.hand])

    def can_survive_attack(self, incoming_damage:int)->bool:
        """
        calculated maximum defense and compares to incoming damage
        """
        max_def = self.calc_max_defense()
        return max_def >= incoming_damage
        
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
    
    def play_all_cards(self)->list[Card]:
        """
        Removes and returns all cards from hand.
        """
        cards = []
        while len(self.hand) > 0:
            cards.append(self.hand.pop())

        return cards
    
    def get_hand_int_values(self)->list[int]:
        self.hand.sort() # always give cards in sorted order
        int_list = [
            card.get_int_value()
            for card in self.hand
        ]
        while len(int_list) < self.hand_limit:
            int_list.append(-1)

        return int_list
    
    def icmd_to_command(self, icmd:str)->str:
        """
        Turns a string of numbers, which correspond to indexes of held cards, into a card string command.
        If icmd tries to access a card that doesn't exist an IndexError will occur
        """
        if icmd == 'yield':
            return 'yield'
        
        self.hand.sort() # hand should already be sorted, sorting again just in case
        cmd_list = [
            self.hand[int(index)-1].get_cmd()
            for index in icmd
        ]
        
        command = ''.join(cmd_list)
        return command

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
        self.is_player_turn = True
        self.running = True
        self.game_result = None
        self.setup_game()

    def setup_game(self):
        """
        Players draw cards until hand limit
        first call of self.next_enemy()
        """
        # Draw initial hand
        
        for player in self.players:
            player.draw_from_deck(self.deck, player.hand_limit)
        
        # Start with the first enemy
        self.next_enemy()
    
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
        max_name_len = max(len(player.name) for player in self.players)
        for player in self.players:
            print(player.name.rjust(max_name_len), f"is holding {player.count_cards_in_hand()}/{player.hand_limit} cards.")
        print()
        print(f"There are {len(self.deck)} cards in the tavern deck.")
        print(f"There are {len(self.discard)} cards in the discard pile.")
        print(f"There are {len(self.enemies)} cards in the Castle deck.")

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

    def player_turn(self):
        self.is_player_turn = True
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
                valid_play = True

            else:
                cmd_list = None
                try:
                    cmd_list = self.active_player.validate_attack_command(command)
                except AssertionError as e:
                    print(e)

                if cmd_list:
                    played_cards = self.active_player.play_cards(cmd_list)
                    self.play_area.add_card(played_cards)
                    self.attack_enemy(played_cards)
                    
                    valid_play = True

    def next_player(self):
        """Increments self.active_player_index then modulo by player count.
        updates self.active_player based on new self.active_player_index."""
        self.active_player_index = (self.active_player_index + 1) % len(self.players)
        self.active_player = self.players[self.active_player_index]

    def enemy_turn(self):
        """On enemy turn, active player must discard cards to withstand enemy attack."""
        self.is_player_turn = False
        print(f"\nIt is {self.current_enemy}'s turn.")
        print(f"{self.active_player.name} must discard cards to withstand {self.current_enemy.attack} damage.")

        if self.current_enemy.attack <= 0:
            print("Enemy attack is 0, no defense needed")
            return None

        if not self.active_player.can_survive_attack(self.current_enemy.attack):
            self.running = False
            self.game_result = 'Lose'
            return None

        print(self.active_player.show_hand())

        valid_play = False
        while not valid_play:
            command = input("\ntype card(s) to defend: ").lower()

            cmd_list = None
            try:
                cmd_list = self.active_player.validate_defend_command(command, self.current_enemy.attack)
            except AssertionError as e:
                print(e)

            if cmd_list:
                played_cards = self.active_player.play_cards(cmd_list)
                self.discard.add_card(played_cards)
                valid_play = True

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
            while card := self.play_area.draw_card():
                # print(f'moving {card} from play area to discard')
                self.discard.add_card(card)
            self.current_enemy = self.enemies.draw_card()
            print(f"\nNew enemy: {self.current_enemy} \n(Health: {self.current_enemy.health})\n(Attack: {self.current_enemy.attack})")
        else:
            print("Congratulations! You've defeated all enemies!")
            self.running = False
            self.game_result = 'Win'
            self.current_enemy = None

    def game_end(self):
        if self.game_result == 'Win':
            print("You won the game!")
        else:
            print("You lost the game.")
        
        print("Thanks for playing!")


if __name__ == "__main__":
    game = RegicideGame(player_names=['Alice','Bob'])
    game.play_game()