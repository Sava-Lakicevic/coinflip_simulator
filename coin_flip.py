# Jordan Peterson talked in a podcast about how in a random system
# people that start with equal amounts of money, one person in the end
# will end up will all of the money, like in Monopoly. Here I model
# people playing "heads or tails", all starting with $10, playing with
# each other. The point is to see the amount of time it takes for
# one person to end up with all of the money

import random


class Player:
    # Each player has a name and starting money, which is set default to $10
    def __init__(self, name, money=10) -> None:
        self.name = name
        self.money = money
    # to_string method implementation

    def __str__(self) -> str:
        return f'{self.name}: {self.money}'


def heads_or_tails(flip):
    # using random uniform distribution we take a random value between 0 and 1.
    # below 0.5 is tails, above is heads. Can be done the other way around as well
    if flip < 0.5:
        return 'TAILS'
    return 'HEADS'


def coin_flip(heads: Player, tails: Player):
    # skip if the player has 0; most often skipping a 'BYE' player.
    # sometimes skipping a busted player that hasn't been removed from
    # the list of players yet.
    if heads.money == 0 or tails.money == 0:
        return
    res = heads_or_tails(random.uniform(0, 1))
    if res == 'HEADS':
        heads.money += 1
        tails.money -= 1
        return
    heads.money -= 1
    tails.money += 1
    return


def a_player_bust(players):
    # checking if a player has busted at the end of each round-robin cycle
    counter = 0
    for player in players:
        if player.money == 0:
            # skipping the 'BYE' player
            if player.name == 'BYE':
                continue
            counter += 1
    # if there is a bust, remove all players with 0 money, including 'BYE'
    if counter > 1:
        for player in players:
            if player.money == 0:
                players.remove(player)
        return True
    return False


def is_over(players):
    # check if the game is over. if more than 1 player has money, the game isn't over
    counter = 0
    for player in players:
        if player.money > 0:
            counter += 1
        if counter > 1:
            return False
    return True


def create_round_robin(players):
    # this function creates a list of all-play-all (round-robin) style tournament list.
    rounds = []
    # add a 'BYE' player if there is an odd number of players.
    if len(players) % 2 == 1:
        players.append(Player('BYE', money=0))

    for i in range(len(players) - 1):
        # divide the player in both halves
        mid = len(players) // 2
        p1 = players[:mid]
        p2 = players[mid:]
        p2.reverse()
        # create a list of all players playing each other.
        for j, k in zip(p1, p2):
            rounds.append([j, k])
        # move the last player at the beginning to ensure everybody is
        # playing against each other.
        players.insert(1, players.pop())
    return rounds


def main():
    players = [
        Player('a'),
        Player('b'),
        Player('c'),
        Player('d'),
        Player('e'),
    ]
    i = 0
    rounds = create_round_robin(players)
    while(not is_over(players)):
        # if a player busts, remove that player and create a new list
        if a_player_bust(players):
            rounds = create_round_robin(players)
        for round in rounds:
            coin_flip(round[0], round[1])
        i += 1
    print(f'It took {i} rounds for 1 player to win.')
    for player in players:
        if player.money > 0:
            print(f'The winner is {player}')


main()
