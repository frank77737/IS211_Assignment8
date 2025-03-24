import random
import time
import argparse
import sys

class Die:
    def __init__(self):
        self.sides = [1, 2, 3, 4, 5, 6]

    def roll(self):
        return random.choice(self.sides)


class Player:
    """Base class for a player in Pig."""
    def __init__(self, name):
        self.name = name
        self.current_points = 0
        self.turn_total = 0
        self.die = Die() 

    def roll(self):
        """Roll the die and return the result."""
        return self.die.roll()

    def hold(self):
        """
        Cumulative turn total to current points and reset turn total.
        """
        self.current_points += self.turn_total
        self.turn_total = 0

    def reset(self):
        """Reset points and turn total to zero."""
        self.current_points = 0
        self.turn_total = 0


class HumanPlayer(Player):
    def decide_action(self):
        while True:
            decision = input(
                f"Hello, {self.name}. Would you like to roll ('r') or hold ('h')? "
            ).strip().lower()

            if decision in ('r', 'h'):
                return decision
            print("Invalid input. Please type 'r' or 'h'.")

class ComputerPlayer(Player):

    def decide_action(self):
        threshold = min(25, 100 - self.current_points)
        if self.turn_total >= threshold:
            return 'h'
        else:
            return 'r'


class PlayerFactory:
    """
    Output a human or computer player
    """
    def create_player(self, name, player_type):
        if player_type.lower() == 'human':
            return HumanPlayer(name)
        elif player_type.lower() == 'computer':
            return ComputerPlayer(name)
        else:
            raise ValueError(
                f"Error player type '{player_type}'. Type human' or 'computer'."
            )


class Game:
    """
    Encapsulates the Pig game logic for two players.
    """
    def __init__(self, player1_type='human', player2_type='human'):
        """
        We create two players using the PlayerFactory and store references
        to the 'current player' and 'other player'.
        """
        factory = PlayerFactory()
        self.player1 = factory.create_player("Player1", player1_type)
        self.player2 = factory.create_player("Player2", player2_type)

        self.current_player = self.player1
        self.other_player = self.player2

    def switch_players(self):
        self.current_player, self.other_player = self.other_player, self.current_player

    def reset_game(self):
        """Reset the game state for both players and set current player to player1."""
        self.player1.reset()
        self.player2.reset()
        self.current_player = self.player1
        self.other_player = self.player2

    def start(self):
        """
        Run the main game loop until one player has 100 or more points.
        Return the winner (Player object).
        """
        print(f"Starting game.")
        print(f"The players are {self.player1.name} and {self.player2.name}.\n")

        while self.player1.current_points < 100 and self.player2.current_points < 100:
        
            decision = self.current_player.decide_action()

            if decision == 'r':
                rolled_num = self.current_player.roll()

                if rolled_num == 1:
                
                    self.current_player.turn_total = 0
                    print(f"{self.current_player.name} rolled a 1 and got no points this turn.")
                    print(f"{self.current_player.name}'s total score: {self.current_player.current_points}\n")
                    self.switch_players()

                else:
                    self.current_player.turn_total += rolled_num
                    print(f"{self.current_player.name} rolled a {rolled_num}.")
                    print(f"Turn total: {self.current_player.turn_total}.  "
                          f"Overall points: {self.current_player.current_points}\n")

            elif decision == 'h':
                self.current_player.hold()
                print(f"{self.current_player.name} chooses to hold.")
                print(f"{self.current_player.name}'s total score: {self.current_player.current_points}\n")
                self.switch_players()

    
        winner = (self.player1 if self.player1.current_points >= 100
                  else self.player2)
        print(f"Congratulations {winner.name}! You have won the game with {winner.current_points} points.")
        return winner


class TimedGameProxy:
    """
    A proxy to the Game class
    """
    def __init__(self, player1_type='human', player2_type='human'):
        self._game = Game(player1_type, player2_type)
        self.start_time = None
        self.time_limit = 60 

    def start(self):
        """
        Follows game logic only difference is a timer
        """
        self.start_time = time.time()
        print(f"60 seconds on the clock play!.")
        print(f"Player One {self._game.player1.name} - Player Two {self._game.player2.name}.\n")

        while (self._game.player1.current_points < 100 and
               self._game.player2.current_points < 100):

        
            elapsed = time.time() - self.start_time
            if elapsed >= self.time_limit:
                print("Time is up")
                break

        
            decision = self._game.current_player.decide_action()

            if decision == 'r':
                rolled_num = self._game.current_player.roll()

                if rolled_num == 1:
                    self._game.current_player.turn_total = 0
                    print(f"{self._game.current_player.name} rolled a 1 and got no points this turn.")
                    print(f"{self._game.current_player.name}'s total score: "
                          f"{self._game.current_player.current_points}\n")
                    self._game.switch_players()

                else:
                    self._game.current_player.turn_total += rolled_num
                    print(f"{self._game.current_player.name} rolled a {rolled_num}.")
                    print(f"Turn total: {self._game.current_player.turn_total}.  "
                          f"Overall points: {self._game.current_player.current_points}\n")

            elif decision == 'h':
                self._game.current_player.hold()
                print(f"{self._game.current_player.name} chooses to hold.")
                print(f"{self._game.current_player.name}'s total score: "
                      f"{self._game.current_player.current_points}\n")
                self._game.switch_players()
    
    
        if self._game.player1.current_points >= 100 or self._game.player2.current_points >= 100:
            winner = (self._game.player1 if self._game.player1.current_points >= 100 else self._game.player2)
        else:
            if self._game.player1.current_points > self._game.player2.current_points:
                winner = self._game.player1
            elif self._game.player2.current_points > self._game.player1.current_points:
                winner = self._game.player2
            else:
            
                print(f"The game ended in a tie. Both players have "
                      f"{self._game.player1.current_points} points.")
                return None

        print(f"You won {winner.name}! With {winner.current_points} points.")
        return winner


def main():
    # Enter below in custom python run 
    # --player1 human --player2 computer --timed     
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1")
    parser.add_argument("--player2")
    parser.add_argument("--timed", action="store_true")
    args = parser.parse_args()

    random.seed(0)

    if args.timed:
        game = TimedGameProxy(args.player1, args.player2)
    else:
        game = Game(args.player1, args.player2)

    game.start()


if __name__ == "__main__":
    main()
