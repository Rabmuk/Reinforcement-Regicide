import itertools
from materials import Card, Deck, Card_Commands
from regicide import RegicideGame
from enum import Enum



class PlayerAgent:
    def __init__(self):
        pass

class RegicideGame_AI(RegicideGame):


    def __init__(self, player_names=['ai_a','ai_b']):
        self.player_names = player_names
        self.action_space = len(Card_Commands.int_to_cmd)
        super().__init__(player_names)
        self.build_action_space()

    def build_action_space(self):
        num_str = ''.join(
            map(str,list(range(1,self.active_player.hand_limit + 1)))
            )
        all_actions = []
        all_actions.append('yield')
        for k in range(1,len(num_str)+1):
            comb = itertools.combinations(num_str, k)
            for c in comb:
                all_actions.append( ''.join(c))

        self.int_to_icmd = all_actions
        self.icmd_to_int = {
            icmd:i
            for i, icmd in enumerate(self.int_to_icmd)
        }
        self.action_space = len(all_actions)

    def check_auto_attack(self)->bool:
        """
        If player has no cards in hand, they're forced to yield.
        Returns True if yield occurs, False if no yield
        """
        if not self.is_player_turn:
            return False
        
        if len(self.active_player.hand) == 0:
            print('Auto yield')
            self.is_player_turn = False
            return True
        # if active player only has 1 card and no other players have cards, play final card
        elif self.active_player.count_cards_in_hand() == 1 and \
            sum([player.count_cards_in_hand() for player in self.players]) == 1:
            print('Attack with last card')
            # play last card
            played_cards = self.active_player.play_all_cards()
            self.play_area.add_card(played_cards)
            self.attack_enemy(played_cards)
            self.is_player_turn = False
            if self.check_enemy_defeated():
                self.is_player_turn = True
            return True
        return False

    def check_auto_defend(self):
        """
        If enemy turn, checks for 0 attack, checks if attack can be survived, then checks if a player must spend all of their cards to defend.
        Calling self.check_full_defend() sets self.running = False if can't be survived
        """
        if self.is_player_turn:
            return None
        
        if self.current_enemy.attack <= 0:
            print('Auto defend no attack')
            self.is_player_turn = True
            self.next_player()
        elif self.check_full_defend():
            if len(self.active_player.hand) == 1 or \
            self.active_player.calc_max_defense() == self.current_enemy.attack:
                print('Auto defend all card(s)')
                self.active_player.play_all_cards()
                self.is_player_turn = True
                self.next_player()
            

    def check_full_defend(self):
        """
        If active player cannot survive and attack, self.running = False and self.game_result = "Lose" and returns False
        If survivable return True
        """
        if not self.active_player.can_survive_attack(self.current_enemy.attack):
            self.running = False
            self.game_result = 'Lose'
            return False
        return True

    def check_no_cards(self):
        """
        If no players have any cards, self.running = False and self.game_result = "Lose".
        This is important to check if enemy attack is 0 but all players are out of cards.
        """
        if sum([len(p.hand) for p in self.players]) == 0:
            print('All players have run out of cards')
            self.running = False
            self.game_result = "Lose"


    def get_state(self):
        """
        get game state as a list of ints
        """
        game_state = [
            len(self.deck),
            len(self.discard),
            len(self.enemies),
            self.current_enemy.get_int_value(),
            self.current_enemy.health,
            self.current_enemy.attack,
            self.is_player_turn,
            self.active_player_index,
            ]
        game_state += [player.count_cards_in_hand() for player in self.players]
        game_state += self.active_player.get_hand_int_values()
        game_state = list(map(int, game_state))
        return game_state

    def reset(self):
        super().__init__(self.player_names)
        return self.get_state(), 'Info'
    
    def step(self, action_int:int):
        reward = 0
        invalid_a = False

        icmd = self.int_to_icmd[action_int]
        try:
            command = self.active_player.icmd_to_command(icmd)
        except IndexError as e:
            # trying to play a card that doesn't exist
            reward = -10
            done = False
            invalid_a = True
            return self.get_state(), reward, done, invalid_a

        # player attacks
        if self.is_player_turn:
            if command.startswith('yeild'):
                print('yield command.')
                self.is_player_turn = False
                exit()
            else:
                try:
                    cmd_list = self.active_player.validate_attack_command(command) # this line will raise an AssertionError if the command is invalid.
                    played_cards = self.active_player.play_cards(cmd_list)
                    self.play_area.add_card(played_cards)
                    self.attack_enemy(played_cards)
                    reward = 1 # successfull attack gives 1 point
                    self.is_player_turn = False
                    if self.check_enemy_defeated():
                        reward = 50
                        self.is_player_turn = True
                except AssertionError as e:
                    # return reward of -1 because command was invalid
                    reward = -10
                    invalid_a = True
            
        # player defends
        else:
            try:
                cmd_list = self.active_player.validate_defend_command(
                    command, self.current_enemy.attack
                    )
                played_cards = self.active_player.play_cards(cmd_list)
                self.discard.add_card(played_cards)
                self.next_player()
                self.is_player_turn = True
                # self.attack_enemy(played_cards)
            except AssertionError as e:
                # return reward of -1 because command was invalid
                reward = -10
                invalid_a = True

        # make any forced moved (like player without cards needing to yield)
        self.check_no_cards()
        # cycles past any players without cards, checking if they can survive and attack
        while self.running and self.check_auto_attack():
            self.check_auto_defend()
            self.check_no_cards()
        # one last check of auto defend
        if self.running:
            self.check_auto_defend()

        done = not self.running
        if done:
            if self.game_result == 'Win':
                reward = 1000
            elif self.game_result == 'Lose':
                reward = -1000
            else:
                raise ValueError('If self.running == False, self.game_result must be "Win" or "Lose"')

        return self.get_state(), reward, done, invalid_a