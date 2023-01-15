import random
import statistics

AVERAGE_IDEOLOGY = 10  # how conservative is the average citizen
NUM_CONTESTANTS = 1024
NUM_SIMULATIONS = 10000


def generate_citizen():
    """
    Generates a random number with uniform distribution between -50 and 50. This represents a citizen's ideology,
    with a positive number indicating more conservative, and negative indicating more liberal.
    We simulate a conservative-dominant district by adding AVERAGE_IDEOLOGY, so the average ideology is shifted.
    Note that the now-conservative citizens were taken from the liberal side, the percentage point gap between the
    two parties becomes simply AVERAGE_IDEOLOGY
    """
    return random.random() * 100 - 50 + AVERAGE_IDEOLOGY


def pair_contestants(contestants) -> list[tuple]:
    """
    randomly pairs contestants by first shuffling the list and then pairing the numbers next to each other
    """
    pairs = list()
    random.shuffle(contestants)
    for i in range(len(contestants)//2):
        pairs.append((contestants[2*i], contestants[2*i+1]))
    return pairs


def elect_candidate(elector, choice1, choice2):
    """
    The elector chooses the choice with the smaller distance from itself
    """
    return min(choice1, choice2, key=lambda c: abs(elector - c))


def run_round(contestants) -> list:
    """
    Pair off the contestants and for each contest, elect the winner
    """
    winners = list()
    for (c1, c2) in pair_contestants(contestants):
        elector = generate_citizen()
        winners.append(elect_candidate(elector, c1, c2))
    return winners


def run_tournament(contestants):
    remaining_contestants = list(contestants)
    while len(remaining_contestants) > 1:
        remaining_contestants = run_round(remaining_contestants)
    winner = remaining_contestants[0]
    return winner


if __name__ == '__main__':
    winners = list()
    contestants = [generate_citizen() for _ in range(NUM_CONTESTANTS)]
    for _ in range(NUM_SIMULATIONS):
        winners.append(run_tournament(contestants))
    avg_winner = sum(winners)/len(winners)
    print("Over", NUM_SIMULATIONS, "tournaments, the average winner is", avg_winner)
    print("The standard deviation of the contestants are", statistics.pstdev(contestants))
    print("The standard deviation of the winners are", statistics.pstdev(winners))
