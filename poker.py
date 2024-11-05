import numpy as np
import random
import time

# Constants for card values and suits
VAL_RANK = {
    2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8",
    9: "9", 10: "10", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace"
}
SUIT_RANK = {1: "Clubs", 2: "Diamonds", 3: "Hearts", 4: "Spades"}

# Score rankings for different hand types
SCORE_RANK = {
    1: "High Card", 2: "Pair", 3: "Two Pair", 4: "Three of a kind",
    5: "The Straight", 6: "The Flush", 7: "The Full House",
    8: "Four of a kind", 9: "The Straight Flush", 10: "The Royal Flush"
}

# Predefined card combinations for poker hands
# List of pairs representing the ranks of cards in poker (1 = Ace, 2 = 2, ..., 4 = 4)
pair_list = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
# List of triplets representing three of a kind card combinations
three_list = [[1, 2, 3], [2, 3, 4], [1, 2, 4], [1, 3, 4]]

# Create a NumPy array for pairs of cards
# For each value from 2 to 14 (Ace), create pairs using the pair_list
pair = np.array([[[val, suit] for pair in pair_list for suit in pair]
                 for val in range(2, 15)])  # Loop through each card value
# Reshape the array to have 78 entries, with each entry containing 2 pairs of suits
pair = np.reshape(pair, (78, 2, 2))

# Create a NumPy array for three of a kind card combinations
three = np.array(
    # Loop through each card value
    [[[val, suit] for three in three_list for suit in three] for val in range(2, 15)])
# Reshape the array to have 52 entries, with each entry containing 3 cards
three = np.reshape(three, (52, 3, 2))

# Create a NumPy array for four of a kind card combinations
# For each value from 2 to 14, create all possible suits (1-4)
four = np.array([[[val, suit] for suit in range(1, 5)]
                 for val in range(2, 15)])  # Loop through each card value

# List of possible straight combinations in poker
straight_list = [
    [14, 2, 3, 4, 5],  # Ace as the highest card in the straight
    [2, 3, 4, 5, 6],   # Straight starting from 2 to 6
    [3, 4, 5, 6, 7],   # Straight from 3 to 7
    [4, 5, 6, 7, 8],   # Straight from 4 to 8
    [5, 6, 7, 8, 9],   # Straight from 5 to 9
    [6, 7, 8, 9, 10],  # Straight from 6 to 10
    [7, 8, 9, 10, 11],  # Straight from 7 to Jack
    [8, 9, 10, 11, 12],  # Straight from 8 to Queen
    [9, 10, 11, 12, 13],  # Straight from 9 to King
    [10, 11, 12, 13, 14]  # Straight from 10 to Ace
]

# Create a NumPy array for straight flush combinations
# For each straight combination, create all possible suits (1-4)
straight_flush = np.array(
    [[[val, suit] for straight in straight_list for val in straight] for suit in range(1, 5)])
# Reshape the array to have 40 entries, with each entry containing 5 cards
straight_flush = np.reshape(straight_flush, (40, 5, 2))

# Create a NumPy array for royal flush combinations
# Royal flush consists of the highest cards (10, Jack, Queen, King, Ace) in each suit
royal_flush = np.array(
    # Loop through each suit
    [[[val, suit] for val in range(10, 15)] for suit in range(1, 5)])


def show_card(cards: set) -> str:
    """Return a string representation of the cards."""
    card_string = ""
    for card in cards:
        card_string += f"({VAL_RANK[card[0]]}, {SUIT_RANK[card[1]]}), "
    return card_string[:-2]  # Remove trailing comma and space


def draw_card(deck_of_cards: set, number_of_cards: int) -> set:
    """Draw a specified number of cards from the deck."""
    cards = set()
    for _ in range(number_of_cards):
        card = random.choice(tuple(deck_of_cards))  # Randomly select a card
        cards.add(card)  # Add card to drawn cards
        deck_of_cards.remove(card)  # Remove card from deck
    return cards


class Player:
    """Class representing a player in the poker game."""
    counter = 1  # Class variable to keep track of player IDs

    def __init__(self, balance: int) -> None:
        """Initialize player with a balance and other attributes."""
        self.id = Player.counter  # Assign player ID
        self.name = ""  # Player's name
        self.balance = balance  # Player's balance
        self.bet = 0  # Current bet
        self.final_score = 0  # Final score after the game
        self.score = 0
        # Current score based on hand ranking
        self.win = 0  # Total winnings
        self.fold_status = False  # Status if player has folded
        self.all_in = False  # Status if player is all in
        self.lose = False  # Status if player has lost
        self.cards = set()  # Cards held by the player
        self.final_cards = set()  # Final cards including community cards
        Player.counter += 1  # Increment player ID counter

    def small_blind(self) -> None:
        """Place a small blind bet."""
        self.bet = 1  # Set bet to small blind amount
        self.balance -= 1  # Deduct from balance

    def big_blind(self) -> None:
        """Place a big blind bet."""
        self.bet = 2  # Set bet to big blind amount
        self.balance -= 2  # Deduct from balance

    def start_bet(self, round_bet: int) -> None:
        """Handle the betting action for the player."""
        while True:
            print("Please enter bet amount!")
            new_bet = input("Action (BET ($) / ALL IN / EXIT) : ").upper()
            try:
                if new_bet == "EXIT":
                    print(f"{self.name} cancels the bet")
                    return -1  # Exit betting
                if new_bet == "ALL IN" and self.balance > 0:
                    self.bet = self.balance  # Bet all remaining balance
                    round_bet = self.bet  # Update round bet
                    self.balance = 0  # Set balance to zero
                    self.all_in = True  # Mark as all in
                    print(f"{self.name} All in (${round_bet})")
                    return round_bet
                else:
                    new_bet = int(new_bet)  # Convert input to integer
                    if self.balance >= new_bet:
                        self.balance -= new_bet  # Deduct bet from balance
                        self.bet = new_bet  # Update bet
                        round_bet = self.bet  # Update round bet
                        print(f"{self.name} raises the bet to ${round_bet}")
                        return round_bet
                    else:
                        # Insufficient balance
                        print("Your balance is not enough!")
            except ValueError:
                print("Invalid bet")  # Handle invalid input

    def raise_bet(self, round_bet: int) -> int:
        """Handle raising the bet."""
        minimum_raise = 4 if round_bet == 2 else round_bet + 1  # Determine minimum raise
        while True:
            print(
                f"Please enter the amount to raise (Minimum to ${minimum_raise})!")
            new_bet = input(f"Action (BET ($) / ALL IN / EXIT) : ").upper()
            try:
                if new_bet == "EXIT":
                    print(f"{self.name} cancels the raise")
                    return -1  # Exit raising
                elif new_bet == "ALL IN" and (minimum_raise - self.bet) <= self.balance:
                    self.bet += self.balance  # Bet all remaining balance
                    round_bet = self.bet  # Update round bet
                    self.balance = 0  # Set balance to zero
                    self.all_in = True  # Mark as all in
                    print(f"{self.name} ALL IN (${round_bet})!")
                    return round_bet
                else:
                    new_bet = int(new_bet)  # Convert input to integer
                    raise_amount = new_bet - self.bet  # Calculate raise amount
                    if new_bet < minimum_raise:
                        print("Bet is too low")  # Raise amount too low
                    elif self.balance >= raise_amount:
                        self.balance -= raise_amount  # Deduct raise from balance
                        self.bet = new_bet  # Update bet
                        round_bet = self.bet  # Update round bet
                        if self.balance == 0:
                            self.all_in = True  # Mark as all in if balance is zero
                            print(f"{self.name} ALL IN (${round_bet})!")
                        else:
                            print(f"{self.name} raises the bet to ${round_bet}")
                        return round_bet
                    else:
                        # Insufficient balance
                        print("Your balance is not enough!")
            except ValueError:
                print("Invalid bet!")  # Handle invalid input

    def call_bet(self, round_bet: int) -> None:
        """Call the current bet."""
        call_amount = round_bet - self.bet  # Calculate call amount
        if self.balance >= call_amount:
            self.balance -= call_amount  # Deduct call amount from balance

            self.bet = round_bet  # Update bet to current round bet
            if self.balance == 0:
                self.all_in = True  # Mark as all in if balance is zero
                print(f"{self.name} ALL IN (${round_bet})!")
            else:
                print(f"{self.name} calls the bet (${round_bet})")
        else:
            self.fold()  # Fold if insufficient balance

    def fold(self) -> None:
        """Fold the player's hand."""
        self.fold_status = True  # Set fold status to True
        print(f"{self.name} folds")  # Notify that the player has folded
        return

    def check(self) -> None:
        """Check the current bet without raising."""
        print(f"{self.name} checks")  # Notify that the player checks
        return

    def __repr__(self) -> str:
        """Return a string representation of the player."""
        message = (f"== {self.name} ==\nBalance: ${self.balance}\nBet: ${
                   self.bet}\nCard: {show_card(self.cards)}")
        return message

    def __len__(self):
        """Return the player's balance."""
        return self.balance

    def __lt__(self, other):
        """Compare players based on their balance."""
        return self.balance > other.balance  # Higher balance is better


class PlayerGroup:
    """Class representing a group of players."""

    def __init__(self, number_of_player: int, initial_balance: int) -> None:
        """Initialize the player group with a specified number of players and their balance."""
        self.players = [Player(initial_balance)
                        for _ in range(number_of_player)]  # Create players
        for player in self.players:
            # Set player names
            player.name = input(f"Player {player.id}'s name: ")

    def remove(self, player: Player) -> None:
        """Remove a player from the group."""
        self.players.remove(player)  # Remove specified player

    def reset_game(self) -> None:
        """Reset the game state for all players."""
        for player in self.players:
            player.win = 0  # Reset wins
            player.score = 0  # Reset score
            player.fold_status = False  # Reset fold status
            player.all_in = False  # Reset all-in status
            player.cards = set()  # Reset cards

    def all_fold(self) -> list[Player]:
        """Return a list of players who have not folded."""
        return [player for player in self.players if not player.fold_status]  # Filter active players

    def all_in(self) -> bool:
        """Check if only one player is left who is not all in."""
        active = [
            player for player in self.players if not player.all_in]  # Get active players
        return len(active) <= 1  # Return True if one or no active players

    def update_status(self):
        """Update the status of players based on their balance."""
        for player in self.players:
            if player.balance < 2:  # If balance is less than 2
                print(f"{player.name} lost! (Balance: ${player.balance})")
                player.lose = True  # Mark player as lost

    def final_score(self):
        """Calculate the final score for each player."""
        for player in self.players:
            player.final_score = player.score * 10  # Calculate final score
        for score in range(3, 0, -1):  # Check scores from high to low
            # Filter players by score
            player_filtered = [
                player for player in self.players if player.score == score]
            while len(player_filtered) > 1:  # If there's a tie
                if score in (3, 2):
                    win = max(player_filtered, key=lambda player: max(
                        check_pair(player.final_cards), key=lambda card: card[0][0]))
                elif score == 1:
                    win = max(player_filtered, key=lambda player: max(
                        player.cards))  # Determine winner
                draw = {player for player in player_filtered if max(
                    player.cards)[0] == max(win.cards)[0]}  # Check for ties
                for player in players:
                    if player in draw:
                        player_filtered.remove(player)  # Remove tied players
                    else:
                        player.final_score -= 1  # Decrease score for non-winners

    def __len__(self) -> None:
        """Return the number of players in the group."""
        return len(self.players)

    def __getitem__(self, index) -> Player:
        """Return a player by index."""
        return self.players[index]

    def __repr__(self) -> str:
        """Return a string representation of the player group."""
        leaderboard = sorted(self.players)  # Sort players by balance
        message = "PLAYERS LEADERBOARD\n===================\n"
        rank = 1
        for player in leaderboard:
            if player.lose:
                # Display lost players
                message += f"{rank}. Player {
                    player.id}: ${player.balance} (Lose)\n"
            else:
                # Display active players
                message += f"{rank}. {player.name}: ${player.balance}\n"
            rank += 1
        return message


class Pot:
    """Class representing the main pot in the game."""

    def __init__(self) -> None:
        """Initialize the pot with a total amount of zero."""
        self.total_pot = 0  # Total amount in the pot

    def add_pot(self, players: PlayerGroup, round_bet: int) -> None:
        """Add bets from players to the pot."""
        for player in players:
            if player.bet > round_bet:
                self.total_pot += round_bet  # Add round bet to pot
                player.bet -= round_bet  # Deduct round bet from player's bet
            else:
                self.total_pot += player.bet  # Add player's bet to pot
                player.bet = 0  # Reset player's bet

    def share(self, number_of_players: int) -> int:
        """Distribute the pot among the winning players."""
        amount = self.total_pot / number_of_players  # Calculate share per player
        self.total_pot = 0  # Reset pot after distribution
        return amount


class SidePot(Pot):
    """Class representing a side pot in the game."""
    counter = 1  # Class variable to keep track of side pot IDs

    def __init__(self, players: list[Player], minimum_bet: int) -> None:
        """Initialize the side pot with players and minimum bet."""
        super().__init__()  # Call parent constructor
        self.id = SidePot.counter  # Assign side pot ID
        self.players = players  # Players contributing to the side pot
        self.total_pot = self.add_pot(players, minimum_bet)  # Add to pot
        SidePot.counter += 1  # Increment side pot ID counter

    def win(self) -> None:
        """Determine the winner of the side pot."""
        leaderboard = sorted(self.players, reverse=True,
                             key=lambda player: player.final_score)  # Sort players by final score
        draw = [player for player in leaderboard if player.final_score ==
                leaderboard[0].final_score]  # Check for ties
        amount = self.share(len(draw))  # Calculate share for winners
        for player in draw:
            print(f"{player.name} wins ${amount} from side pot {
                  self.id}")  # Announce winner
            player.win += amount  # Add winnings to player's total

    def __repr__(self) -> str:
        """Return a string representation of the side pot."""
        players = [
            f"{player.name}" for player in self.players]  # List player names
        return f"Side Pot {self.id} {players}: ${self.total_pot}"


class MainPot(Pot):
    """Class representing the main pot in the game."""

    def add_pot(self, players: PlayerGroup, round_bet: int) -> None:
        """Add bets from players to the main pot."""
        super().add_pot(players, round_bet)  # Call parent method
        return self.add_side_pot(players)  # Add side pots

    def add_side_pot(self, players: PlayerGroup) -> list[SidePot]:
        """Create side pots based on player bets."""
        side = []  # List to hold side pots
        while True:
            side_pot_player = []  # List of players for the current side pot
            for player in players:
                if player.bet > 0:
                    # Add player to side pot if they have a bet
                    side_pot_player.append(player)
            if len(side_pot_player) > 0:
                # Find player with minimum bet
                minimum_bet = min(side_pot_player, key=lambda x: x.bet)
                # Create a new side pot
                side.append(SidePot(side_pot_player, minimum_bet))
                continue
            else:
                return side  # Return list of side pots

    def win(self, leaderboard: list[Player]) -> None:
        """Determine the winner of the main pot."""
        draw = [player for player in leaderboard if player.final_score ==
                leaderboard[0].final_score]  # Check for ties
        amount = self.share(len(draw))  # Calculate share for winners
        for player in draw:
            # Announce winner
            print(f"{player.name} wins ${amount} from main pot")
            player.win += amount  # Add winnings to player's total

    def __repr__(self) -> str:
        """Return a string representation of the main pot."""
        return f"Main Pot: ${self.total_pot}"


def turns(players: PlayerGroup, start_player: int, repeat_turn: int):
    """Generator to iterate through players' turns."""
    index = start_player  # Start from the specified player
    turn_taken = 0  # Count of turns taken

    # Loop until all players have taken their turn
    while turn_taken < len(players) - repeat_turn:
        player = players[index]  # Get the current player

        if not player.fold_status and not player.all_in:  # If player is active
            yield (index, player)  # Yield current player's index and object
        elif players[index].fold_status:
            # Notify if player has folded
            print(f"Player {players[index].id} skipped (Fold)")
        elif players[index].all_in:
            # Notify if player is all in
            print(f"Player {players[index].id} skipped (All in)")

        index = (index + 1) % len(players)  # Move to the next player
        turn_taken += 1  # Increment turn count

    return


def blind(players: PlayerGroup, small_blind: int, big_blind: int) -> int:
    """Set the small and big blind bets for the players."""
    players[small_blind].small_blind(
    )  # Player in small blind position places bet
    if big_blind >= 0:
        # Player in big blind position places bet
        players[big_blind].big_blind()
        # Determine next player to act
        next_turn = (big_blind + 1) % len(players)
        return next_turn
    else:
        # Move to the next player if no big blind
        small_blind = (small_blind + 1) % len(players)
        return small_blind


def act(player: Player, preflop: bool, round_bet: int) -> int:
    """Handle the player's action during their turn."""
    if round_bet in (1, 2) and not preflop:  # If it's not preflop
        while True:
            # Prompt for action
            action = input("Action (CHECK / BET / FOLD): ")
            if action.upper() == "CHECK":
                player.check()  # Player checks
                return round_bet
            elif action.upper() == "BET":
                start_bet_amount = player.start_bet(
                    round_bet)  # Player starts betting
                if start_bet_amount == -1:
                    continue  # If canceled, continue prompting
                return start_bet_amount
            elif action.upper() == "FOLD":
                player.fold()  # Player folds
                return round_bet
            else:
                print("Invalid Input!")  # Handle invalid input
    else:
        while True:
            # Prompt for action
            action = input("Action (CALL / RAISE / FOLD): ")
            if action.upper() == "CALL":
                player.call_bet(round_bet)  # Player calls the bet
                return round_bet
            elif action.upper() == "RAISE":
                raise_amount = player.raise_bet(
                    round_bet)  # Player raises the bet
                if raise_amount == -1:
                    continue  # If canceled, continue prompting
                return raise_amount
            elif action.upper() == "FOLD":
                player.fold()  # Player folds
                return round_bet
            else:
                print("Invalid Input!")  # Handle invalid input


def round_decorator(round_count: int):
    """Decorator to announce the betting round and deal community cards."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if round_count == 1:
                print("Second Betting Round: The Flop")
                print("==============================")
            elif round_count == 2:
                print("Third Betting Round: The Turn")
                print("=============================")
            elif round_count == 3:
                print("Final Betting Round: The River")
                print("==============================")
            print("Dealing Community Cards...")
            print()
            side = func(*args, **kwargs)  # Call the decorated function
            return side
        return wrapper
    return decorator


def preflop(players: PlayerGroup, deck_of_cards: set, main: MainPot, start_player: int, round_bet: int) -> list[SidePot]:
    """Handle the pre flop betting round."""
    print("First Betting Round: Preflop")
    print("============================")

    print("Drawing Card...")
    time.sleep(0.5)  # Simulate delay for drawing cards
    print()
    for player in players:
        player.cards = draw_card(deck_of_cards, 2)  # Each player draws 2 cards

    repeat_turn = 0  # Initialize turn repeat counter
    while True:
        round_over = True  # Flag to check if the round is over
        for player in turns(players, start_player, repeat_turn):
            print(f"Total Pot: ${main.total_pot}")  # Display total pot
            # Display current round bet
            print(f"Current Round Bet: ${round_bet}")
            print(player[1])  # Show player's information
            raise_bet = act(player[1], True, round_bet)  # Get player's action
            print()
            if raise_bet != round_bet:  # If the bet has changed
                round_bet = raise_bet  # Update round bet
                # Move to the next player
                start_player = (player[0] + 1) % len(players)
                round_over = False  # Round is not over
                repeat_turn = 1  # Set repeat turn flag
                break
            last_player = players.all_fold()  # Check if all players have folded
            if len(last_player) == 1:  # If only one player is left
                return main.add_pot(players, round_bet)  # Add pot and return
        if round_over:  # If the round is over
            return main.add_pot(players, round_bet)  # Add pot and return


def round(players: PlayerGroup, deck_of_cards: set, community_card: set, main: MainPot, start_player: int, round_bet: int, number_of_cards: int):
    """Handle a betting round after the preflop."""
    community_card.update(
        draw_card(deck_of_cards, number_of_cards))  # Draw community cards
    turn = 0  # Initialize turn counter
    while True:
        round_over = True  # Flag to check if the round is over
        for player in turns(players, start_player, turn):
            print("Community Cards")
            print(show_card(community_card))  # Show community cards
            print("=" * len(show_card(community_card)))  # Separator
            print(f"Total Pot: ${main.total_pot}")  # Display total pot
            # Display current round bet
            print(f"Current Round Bet: ${round_bet}")
            print(player[1])  # Show player's information
            raise_bet = act(player[1], False, round_bet)  # Get player's action
            print()
            if raise_bet != round_bet:  # If the bet has changed
                round_bet = raise_bet  # Update round bet
                # Move to the next player
                start_player = (player[0] + 1) % len(players)
                round_over = False  # Round is not over
                turn = 1  # Set turn flag
                break
            last_player = players.all_fold()  # Check if all players have folded
            if len(last_player) == 1:  # If only one player is left
                return main.add_pot(players, round_bet)  # Add pot and return
        if round_over:  # If the round is over
            return main.add_pot(players, round_bet)  # Add pot and return


@round_decorator(1)
def flop(players: PlayerGroup, deck_of_cards: set, community_card: set, main: MainPot, start_player: int, round_bet: int):
    """Handle the flop betting round."""
    return round(players, deck_of_cards, community_card, main, start_player, round_bet, 3)  # Draw 3 community cards


@round_decorator(2)
def turn(players: PlayerGroup, deck_of_cards: set, community_card: set, main: MainPot, start_player: int, round_bet: int):
    """Handle the turn betting round."""
    return round(players, deck_of_cards, community_card, main, start_player, round_bet, 1)  # Draw 1 community card


@round_decorator(3)
def river(players: PlayerGroup, deck_of_cards: set, community_card: set, main: MainPot, start_player: int, round_bet: int):
    """Handle the river betting round."""
    return round(players, deck_of_cards, community_card, main, start_player, round_bet, 1)
# Draw 1 community card


def check_set(player_hand: set, array: np.array) -> bool:
    """Check if the player's hand contains any of the specified sets."""
    for card in array:
        card = list(tuple(x) for x in card)  # Convert to list of tuples
        card = {(int(x), int(y)) for x, y in card}  # Convert to set of tuples
        # Check if the player's hand contains the card set
        result = card.issubset(player_hand)
        if result:
            return True  # Return True if found
    return False  # Return False if not found


def check_pair(player_hand: set) -> int:
    """Check for pairs in the player's hand."""
    pair = []  # List to hold pairs
    for card in pair:
        card = list(tuple(x) for x in card)  # Convert to list of tuples
        card = {(int(x), int(y)) for x, y in card}  # Convert to set of tuples
        # Check if the player's hand contains the card set
        result = card.issubset(player_hand)
        if result:
            pair.append(list(card))  # Add found pair to the list
    return pair  # Return the list of pairs


def check_result(player_hand: set, community_card: set) -> int:
    """Evaluate the player's hand against the community cards and return the hand rank."""
    flush = [x for x in range(1, 5) if [card[1] for card in player_hand].count(
        x) >= 5]  # Check for flush
    # Get unique card values from player's hand
    straight_player = {card[0] for card in player_hand}
    straight = [card for card in straight_list if set(
        card).issubset(straight_player)]  # Check for straight
    if check_set(player_hand, royal_flush):
        return 10  # Royal Flush
    elif check_set(player_hand, straight_flush):
        return 9  # Straight Flush
    elif check_set(player_hand, four):
        return 8  # Four of a Kind
    elif check_set(player_hand, three) and check_set(player_hand, pair):
        return 7  # Full House
    elif len(flush) > 0:
        return 6  # Flush
    elif len(straight) > 0:
        return 5  # Straight
    elif check_set(player_hand, three):
        return 4  # Three of a Kind
    elif len(check_pair(player_hand)) == 2 and len(check_pair(community_card)) != 2:
        return 3  # Two Pair
    elif len(check_pair(player_hand)) in (1, 3):
        return 2  # One Pair
    else:
        return 1  # High Card


def showdown(players: PlayerGroup, community_card: set, main: MainPot, side: list[SidePot]):
    """Conduct the showdown to determine the winner."""
    print("S H O W D O W N")
    print("===============")
    if community_card:
        print("Community Card")
        print(show_card(community_card))  # Show community cards
        print()
    for player in players:
        if not player.fold_status:  # If player has not folded
            # Combine player's cards with community cards
            player.final_cards = player.cards | community_card
            player.score = check_result(
                player.final_cards, community_card)  # Evaluate player's hand
            print(f"{player.name} Final Card")
            print(show_card(player.final_cards))  # Show final cards
            # Show player's cards
            print(f"{player.name} Cards: {show_card(player.cards)}")
            print(f"Card Rank: {SCORE_RANK[player.score]}")  # Show hand rank
            time.sleep(1)  # Pause for effect
            print()

    players.final_score()  # Calculate final scores

    # Sort players by final score
    leaderboard = sorted(players, reverse=True,
                         key=lambda player: player.final_score)

    print(main)  # Show main pot
    main.win(leaderboard)  # Determine winner of the main pot

    if len(side) > 0:  # If there are side pots
        for sides in side:
            print(sides)  # Show side pot information
            sides.win()  # Determine winner of the side pot

    print()
    print("CARD RANK LEADERBOARD")
    print("================")
    rank = 1
    for player in leaderboard:
        if player.fold_status:
            print(f"{rank}. {player.name} (Fold)")  # Show folded players
        else:
            # Show active players and their winnings
            print(f"{rank}. {player.name} ({
                  SCORE_RANK[player.score]}) +${player.win}")
        player.balance += player.win  # Update player's balance with winnings
        rank += 1  # Increment rank for next player

    time.sleep(1)  # Pause for effect
    print()  # Print a new line


def game(players: PlayerGroup) -> None:
    """Main game loop to handle the flow of the poker game."""
    button = 0  # Initialize button position
    while True:
        # Create a deck of cards
        deck_of_cards = {(val, suit) for suit in SUIT_RANK for val in VAL_RANK}
        community_card = set()  # Initialize community cards

        main = MainPot()  # Create the main pot
        side = []  # Initialize side pots
        round_bet = 1  # Set initial round bet

        # Determine small blind position
        small_blind = (button + 1) % len(players)
        if len(players) > 2:
            # Determine big blind position
            big_blind = (small_blind + 1) % len(players)
        else:
            big_blind = -1  # No big blind if only two players

        print("POSITION")
        print(f"Button: {players[button].name}")  # Display button player
        # Display small blind player
        print(f"Small Blind: {players[small_blind].name}")
        if len(players) > 2:
            round_bet = 2  # Set round bet to 2 if there is a big blind
            # Display big blind player
            print(f"Big Blind: {players[big_blind].name}")

        time.sleep(1)  # Pause for effect

        print()
        print("Starting Game...")
        print()

        time.sleep(0.5)  # Simulate delay for starting the game

        # Set blinds and determine starting player
        start_player = blind(players, small_blind, big_blind)

        side += preflop(players, deck_of_cards, main,
                        start_player, round_bet)  # Handle preflop betting

        start_player = small_blind  # Reset starting player to small blind

        if len(players.all_fold()) > 1 and not players.all_in():  # If more than one player is active
            side += flop(players, deck_of_cards, community_card,
                         main, start_player, round_bet)  # Handle flop betting

        if len(players.all_fold()) > 1 and not players.all_in():  # If more than one player is active
            side += turn(players, deck_of_cards, community_card,
                         main, start_player, round_bet)  # Handle turn betting

        if len(players.all_fold()) > 1 and not players.all_in():  # If more than one player is active
            side += river(players, deck_of_cards, community_card,
                          main, start_player, round_bet)  # Handle river betting

        showdown(players, community_card, main, side)  # Conduct the showdown

        players.update_status()  # Update player statuses

        # Display Leaderboard
        print(players)  # Show player standings

        time.sleep(1)  # Pause for effect

        for player in players:
            if player.lose:  # If player has lost
                players.remove(player)  # Remove player from the game

        if len(players) < 2:  # If less than two players remain
            print("Winner of This Game")
            print("===================")
            print(f"Congratulations to {players[0].name}!")  # Announce winner
            return  # End the game

        # Ask if players want to continue
        play_again = input("Do you want to continue to next game? (Y/N) ")
        print()
        if play_again.upper() == "Y":
            # Move button to the next player
            button = (button + 1) % len(players)
            players.reset_game()  # Reset game state for players
            continue  # Start a new game
        else:
            leaderboard = sorted(players)  # Sort players for final leaderboard
            print("Winner of This Game")
            print("===================")
            # Announce final winner
            print(f"Congratulations to {leaderboard[0].name}!")
            return  # End the game


if __name__ == "__main__":
    print("Welcome to Texas Hold'em Poker Game")
    print("===================================")

    while True:
        try:
            # Prompt for number of players
            number_of_player = int(input("Enter Number of Player (2-10): "))

            if number_of_player < 2 or number_of_player > 10:
                # Validate player count
                print("Invalid number of player (2-10)!")
            else:
                break  # Exit loop if valid input
        except ValueError:
            print("Input must be an integer!")  # Handle non-integer input

    print()

    initial_balance = 10  # Default initial balance for players
    print(f"Default Initial Balance for All Player is ${initial_balance}")
    custom_initial_balance = input(
        # Ask for custom balance
        "Do you want to custom initial balance? (Y/N) ")
    if custom_initial_balance.upper() == "Y":
        while True:
            try:
                # Prompt for custom balance
                initial_balance = int(input("Enter Initial Balance $: "))
                break  # Exit loop if valid input
            except ValueError:
                # Handle non-integer input
                print("Balance must be an integer!")
    print(f"Initial Balance is set to ${initial_balance}")

    print()

    # Create player group
    players = PlayerGroup(number_of_player, initial_balance)

    print()
    print("Loading Game...")
    print()
    time.sleep(0.5)  # Simulate loading delay

    game(players)  # Start the game

    print()
    print("Thank you for playing")  # End of game message
    print("See you in the next game!")  # Farewell message
