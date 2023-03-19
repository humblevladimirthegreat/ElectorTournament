import random
import statistics
# import matplotlib.pyplot as plot  # uncomment to see histogram

PERCENT_CONSERVATIVE = .6  # how many conservatives are there
NUM_CONTESTANTS = 1024
NUM_SIMULATIONS = 1000
DISTRIBUTION_MEAN = 30
STANDARD_DEVIATION = 10

def generate_citizen():
    """
    Generates a random number which represents a citizen's ideology,
    with a positive number indicating more conservative, and negative indicating more liberal.
    We simulate more partisanship by using a bimodal distribution.
    We simulate a conservative-dominant district by using PERCENT_CONSERVATIVE
    """
    mean = DISTRIBUTION_MEAN if random.random() < PERCENT_CONSERVATIVE else -DISTRIBUTION_MEAN
    return random.normalvariate(mu=mean, sigma=STANDARD_DEVIATION)

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
    The elector picks the choice with the smallest distance from itself
    """
    return min(choice1, choice2, key=lambda c: abs(elector - c))

def run_round(contestants) -> list:
    """
    Pair off the contestants and for each contest, elect the winner. Returns all the winners of this round.
    """
    winners = list()
    for (c1, c2) in pair_contestants(contestants):
        elector = generate_citizen()
        winners.append(elect_candidate(elector, c1, c2))
    return winners

def run_tournament(contestants):
    """
    Run a single tournament with the given contestant. Returns the winner
    """
    remaining_contestants = list(contestants)
    while len(remaining_contestants) > 1:
        remaining_contestants = run_round(remaining_contestants)
    winner = remaining_contestants[0]
    return winner

if __name__ == '__main__':
    winners = list()
    contestants = [generate_citizen() for _ in range(NUM_CONTESTANTS)]
    print("The average contestant has ideology of", sum(contestants)/len(contestants))
    contestants *= 4 # each candidate is entered 4 times to simulate multi-elimination
    for _ in range(NUM_SIMULATIONS):
        winners.append(run_tournament(contestants))
    print("Over", NUM_SIMULATIONS, "tournaments, the average winner is", sum(winners)/len(winners))
    print("The standard deviation of the contestants are", statistics.pstdev(contestants))
    print("The standard deviation of the winners are", statistics.pstdev(winners))
    print("The minority was elected", sum(map(lambda x: x < 0, winners))/len(winners) * 100, "%")
    print("Solid members were elected", sum(map(lambda x: abs(x) > 30, winners))/len(winners) * 100, "%")
    print("Staunch members were elected", sum(map(lambda x: abs(x) > 40, winners))/len(winners) * 100, "%")
    # uncomment to save histograph
    # plot.hist(winners)
    # plot.savefig('tournament_lottery_voting.png')
