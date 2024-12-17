import random


class Coin:
    def __init__(self, min_value, max_value, is_red=False):
        self.min_value = min_value
        self.max_value = max_value
        self.is_red = is_red  # Red coins always land max value

    def flip(self):
        """Simulate flipping a coin, returning its value."""
        return self.max_value if self.is_red else random.randint(self.min_value, self.max_value)


class Card:
    def __init__(self, name, card_type, coins, special_effect=None):
        self.name = name
        self.card_type = card_type  # 'attack', 'defense', etc.
        self.coins = coins  # List of Coin objects
        self.special_effect = special_effect  # Custom effect function

    def play(self, combatant, opponent, clash_winner=None):
        """Flip all coins on the card and apply any special effects."""
        coin_values = [coin.flip() for coin in self.coins]
        if self.special_effect:
            self.special_effect(combatant, opponent, clash_winner)
        return coin_values


class Combatant:
    def __init__(self, name, deck, is_player=False):
        self.name = name
        self.deck = deck  # List of Card objects
        self.hp = 100
        self.ego_turns = 0  # Turns remaining for Manifest: E.G.O effect
        self.is_player = is_player  # Identify if this combatant is the player

    def choose_card(self):
        """Let the player select a card or auto-pick for AI."""
        if self.is_player:
            print("\nYour cards:")
            for i, card in enumerate(self.deck):
                print(f"{i + 1}: {card.name} ({card.card_type})")

            # Input validation loop
            while True:
                try:
                    choice = int(input(f"Choose a card to play (1-{len(self.deck)}): ")) - 1
                    if 0 <= choice < len(self.deck):
                        return self.deck[choice]
                    else:
                        print(f"Please enter a number between 1 and {len(self.deck)}.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        else:
            return random.choice(self.deck)  # AI randomly selects a card

    def apply_ego(self):
        """Applies Manifest: E.G.O effect to the combatant's deck."""
        if self.ego_turns > 0:
            print(f"{self.name} is under the Manifest: E.G.O effect!")
            for card in self.deck:
                card.coins.append(Coin(1, 6))  # Adds an extra regular coin
            self.ego_turns -= 1


def manifest_ego(combatant, opponent, clash_winner=None):
    """Special effect for Manifest: E.G.O."""
    print(f"{combatant.name} activates Manifest: E.G.O!")
    combatant.ego_turns = 3


def o_dullahana_effect(combatant, opponent, clash_winner=None):
    """Special effect for O Dullahana...!"""
    print(f"{combatant.name} blocks with O Dullahana...!")
    if clash_winner == combatant.name:
        print(f"{combatant.name} counters with a two-coin attack!")
        opponent.hp -= sum(Coin(2, 5, True).flip() for _ in range(2))


def clash(coins1, coins2):
    """Simulate a clash between two players' coin rolls."""
    while coins1 and coins2:
        roll1 = sum(coins1)
        roll2 = sum(coins2)
        print(f"Clash rolls: Player: {roll1} vs Enemy: {roll2}")

        if roll1 > roll2:
            print("Player wins the clash round!")
            coins2.pop()  # Enemy loses one coin
        elif roll2 > roll1:
            print("Enemy wins the clash round!")
            coins1.pop()  # Player loses one coin
        else:
            print("It's a tie! No coins lost.")

        print(f"Remaining coins: Player: {len(coins1)}, Enemy: {len(coins2)}")

    # Determine the winner
    return "player" if coins2 == [] else "enemy"


def combat_round(combatant1, combatant2):
    """Simulate a single combat round with user-selected cards and clashing."""
    combatant1.apply_ego()
    combatant2.apply_ego()

    card1 = combatant1.choose_card()
    card2 = combatant2.choose_card()

    print(f"\n{combatant1.name} plays {card1.name}")
    print(f"{combatant2.name} plays {card2.name}")

    coins1 = card1.play(combatant1, combatant2)
    coins2 = card2.play(combatant2, combatant1)

    print(f"Initial rolls: Player: {sum(coins1)} | Enemy: {sum(coins2)}")
    winner = clash(coins1, coins2)

    # Pass clash winner to cards' special effects
    card1.play(combatant1, combatant2, winner)
    card2.play(combatant2, combatant1, winner)

    # Damage is calculated based on final remaining coins
    damage = abs(sum(coins1) - sum(coins2))
    if winner == "player":
        combatant2.hp -= damage
        print(f"Enemy loses {damage} HP!")
    else:
        combatant1.hp -= damage
        print(f"Player loses {damage} HP!")

    print(f"\nPlayer HP: {combatant1.hp}")
    print(f"Enemy HP: {combatant2.hp}")


# Define the deck of 10 cards
def build_deck():
    coin1 = Coin(1, 6)
    coin2 = Coin(2, 5)
    red_coin = Coin(4, 4, is_red=True)  # Red coin always lands on 4

    return [
        Card("Slash", "attack", [coin1, coin2]),
        Card("Impale", "attack", [coin2, coin2]),
        Card("Greater Slash", "attack", [coin1, coin1, coin1]),
        Card("Great Slash: Horizontal", "attack", [coin1, coin1], lambda c, o, w: print("Damage x coins!")),
        Card("Great Slash: Vertical", "attack", [coin1, coin1, coin1, coin1]),
        Card("Manifest: E.G.O", "support", [], manifest_ego),
        Card("O Dullahana...!", "defense", [red_coin], o_dullahana_effect),
        Card("Block", "defense", [red_coin]),
        Card("Counter", "counter", [coin2], lambda c, o, w: print(f"{c.name} counters!")),
        Card("Shield Bash", "attack", [coin1, coin1]),
    ]


# Define the specific deck for each enemy
def red_mist_deck():
    coin1 = Coin(1, 6)
    coin2 = Coin(2, 5)
    red_coin = Coin(4, 4, is_red=True)
    return [
        Card("Greater Slash: Vertical", "attack", [coin1, coin1, coin1, coin1]),
        Card("Greater Slash: Horizontal", "attack", [coin1, coin1]),
        Card("Manifest: E.G.O", "support", [], manifest_ego),
        Card("Impale", "attack", [coin2, coin2]),
        Card("Block", "defense", [red_coin]),
    ]

def r_corp_rabbit_deck():
    coin1 = Coin(1, 6)
    coin2 = Coin(2, 5)
    return [
        Card("Impale", "attack", [coin2, coin2]),
        Card("Slash", "attack", [coin1, coin2]),
        Card("Greater Slash", "attack", [coin1, coin1, coin1]),
        Card("Great Slash: Vertical", "attack", [coin1, coin1, coin1, coin1]),
    ]

def random_guy_deck():
    coin1 = Coin(1, 6)
    coin2 = Coin(2, 5)
    red_coin = Coin(4, 4, is_red=True)
    return [
        Card("Slash", "attack", [coin1, coin2]),
        Card("Impale", "attack", [coin2, coin2]),
        Card("Block", "defense", [red_coin]),
        Card("O Dullahana...!", "defense", [red_coin], o_dullahana_effect),
    ]


# Main Combat Simulation
def main():
    full_deck = build_deck()

    # Let the player select 4 cards for their deck
    print("Select 4 cards from the full deck:")
    selected_cards = []
    remaining_cards = full_deck.copy()

    for i in range(4):
        print(f"\nRemaining cards ({len(remaining_cards)}):")
        for index, card in enumerate(remaining_cards):
            print(f"{index + 1}: {card.name} ({card.card_type})")

        while True:
            try:
                choice = int(input(f"Choose card {i + 1} to add to your deck (1-{len(remaining_cards)}): ")) - 1
                if 0 <= choice < len(remaining_cards):
                    selected_cards.append(remaining_cards.pop(choice))
                    break
                else:
                    print(f"Please enter a number between 1 and {len(remaining_cards)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    # Let the player choose the enemy encounter
    print("\nChoose your enemy encounter:")
    print("1: Red Mist")
    print("2: R Corp Rabbit")
    print("3: Random Guy")
    enemy_choice = input("Enter your choice (1-3): ")

    if enemy_choice == '1':
        enemy_deck = red_mist_deck()
        enemy_name = "Red Mist"
    elif enemy_choice == '2':
        enemy_deck = r_corp_rabbit_deck()
        enemy_name = "R Corp Rabbit"
    else:
        enemy_deck = random_guy_deck()
        enemy_name = "Random Guy"

    # Instantiate player and enemy combatants
    player = Combatant("Player", selected_cards, is_player=True)
    enemy = Combatant(enemy_name, enemy_deck)

    # Combat loop
    while player.hp > 0 and enemy.hp > 0:
        combat_round(player, enemy)

    if player.hp > enemy.hp:
        print("\nPlayer wins!")
    elif enemy.hp > player.hp:
        print("\nEnemy wins!")
    else:
        print("\nIt's a draw!")


if __name__ == "__main__":
    main()
