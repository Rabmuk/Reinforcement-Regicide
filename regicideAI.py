from materials import Card, Deck, Card_Commands
from regicide import RegicideGame
from enum import Enum



class PlayerAgent:
    def __init__(self):
        pass

class RegicideGame_AI(RegicideGame):


    def __init__(self, player_names=['ai_a','ai_b']):
        self.player_names = player_names
        self.action_space = Discrete(Card_Commands.int_to_cmd)
        super().__init__(player_names)

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
            ]
        game_state += [player.count_cards_in_hand() for player in self.players]
        game_state += self.active_player.get_bool_list_cards()
        game_state = list(map(int, game_state))
        return game_state

    def reset(self):
        super().__init__(self.player_names)
        return self.get_state(), 'Info'
    
    def step(self, int_list:list[int]):
        reward = 0

        command = Card_Commands.int_list_to_cmd(int_list)

        # player attacks
        if self.is_player_turn:
            # TODO: implement yield
            if command.startswith('yeild_'):
                print('yield command.')
                self.is_player_turn = False
            else:
                try:
                    cmd_list = self.active_player.validate_attack_command(command) # this line will raise an AssertionError if the command is invalid.
                    played_cards = self.active_player.play_cards(cmd_list)
                    self.play_area.add_card(played_cards)
                    self.attack_enemy(played_cards)
                    reward = 1 # successfull attack gives 1 point
                    self.is_player_turn = False
                    if self.check_enemy_defeated():
                        reward = 11
                        self.is_player_turn = True
                except AssertionError as e:
                    # return reward of -1 because command was invalid
                    reward = -1
            # after attack checks if player can survive an attack
            if not self.active_player.can_survive_attack(self.current_enemy.attack):
                self.running = False
                self.game_result = 'Lose'
        # player defends
        else:
            try:
                cmd_list = self.active_player.validate_defend_command(
                    command, self.current_enemy.attack
                    )
                played_cards = self.active_player.play_cards(cmd_list)
                self.discard.add_card(played_cards)
                self.next_player()
                # self.attack_enemy(played_cards)
            except AssertionError as e:
                # return reward of -1 because command was invalid
                reward = -1


        done = not self.running
        if done:
            if self.game_result == 'Win':
                reward = 100
            if self.game_result == 'Lose':
                reward = -10

        return self.get_state(), reward, done