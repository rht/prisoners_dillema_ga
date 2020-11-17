# Make sure to read this paper https://www.cs.umd.edu/~golbeck/downloads/JGolbeck_prison.pdf

import random

# strategies
def always_cooperate(hist, side):
    return True

def always_defect(hist, side):
    return False

def do_random(hist, side):
    return random.random() > 0.5

def tit_for_tat(hist, side):
    if side == 1:
        return hist[-1]
    else:
        return hist[-2]

# the rest of the implementation
def get_payoff(action1, action2):
    if action1 and action2:
        return 3, 3
    elif action1 and not action2:
        return 0, 5
    elif not action1 and action2:
        return 5, 0
    else:
        return 1, 1

def get_strategy_str(strat):
    representation = []
    # True means cooperate, False means defect
    for i in [True, False]:
        for j in [True, False]:
            for k in [True, False]:
                for l in [True, False]:
                    for m in [True, False]:
                        for n in [True, False]:
                            action = strat([i, j, k, l, m, n], 1)
                            representation.append(action)
    return representation

def play_a_game(hist, strat1, strat2):
    action1 = strat1(hist, 1)
    action2 = strat2(hist, 2)
    return get_payoff(action1, action2)

def play_a_round(strat1, strat2):
    cum_payoff1, cum_payoff2 = 0, 0
    for i in [True, False]:
        for j in [True, False]:
            for k in [True, False]:
                for l in [True, False]:
                    for m in [True, False]:
                        for n in [True, False]:
                            payoff1, payoff2 = play_a_game([i, j, k, l, m, n], strat1, strat2)
                            cum_payoff1 += payoff1
                            cum_payoff2 += payoff2
    return cum_payoff1, cum_payoff2

def create_offsprings(parent1, parent2):
    size = len(parent1)
    crossover_idx = random.randint(1, size - 1)
    offspring1 = parent1[:crossover_idx] + parent2[crossover_idx:]
    offspring2 = parent2[:crossover_idx] + parent1[crossover_idx:]

    def mutate(dna):
        if random.random() < 0.05:  # 5%
            loc = random.randint(0, len(dna) - 1)
            dna[loc] = not dna[loc]
        return dna
    offspring1 = mutate(offspring1)
    offspring2 = mutate(offspring2)
    return offspring1, offspring2

hist2idx_dict = {}
count = 0
for i in [True, False]:
    for j in [True, False]:
        for k in [True, False]:
            for l in [True, False]:
                for m in [True, False]:
                    for n in [True, False]:
                        hist2idx_dict[(i, j, k, l, m, n)] = count
                        count += 1

def str_to_strat(_str):
    def strat(hist, side):
        if side == 1:
            return _str[hist2idx_dict[tuple(hist)]]
        else:  # 2
            _flipped_hist = [hist[1], hist[0], hist[3], hist[2], hist[5], hist[4]]
            return _str[hist2idx_dict[tuple(_flipped_hist)]]
    return strat

def play_a_cycle(population):
    pairs = []
    size = len(population)
    payoffs = [0 for i in range(size)]
    for i in range(size):
        for j in range(size):
            if i == j:
                continue
            if i < j:
                pair = (i, j)
            if i > j:
                pair = (j, i)
            if pair not in pairs:
                pairs.append(pair)
    # Play against each other
    for pair in pairs:
        strat1 = str_to_strat(population[pair[0]])
        strat2 = str_to_strat(population[pair[1]])
        payoff1, payoff2 = play_a_round(strat1, strat2)
        payoffs[pair[0]] += payoff1
        payoffs[pair[1]] += payoff2
    system_payoff = sum(payoffs)
    print('system payoff', system_payoff)
    # Only the top half of the population can create offsprings
    selected_parents = []
    while len(selected_parents) < size / 2:
        max_payoff = max(payoffs)
        idx = payoffs.index(max_payoff)
        payoffs.pop(idx)
        selected_parents.append(population.pop(idx))
    offsprings = []
    while len(selected_parents) > 0:
        random.shuffle(selected_parents)
        parent1 = selected_parents.pop()
        random.shuffle(selected_parents)
        parent2 = selected_parents.pop()
        offspring1, offspring2 = create_offsprings(parent1, parent2)
        offsprings.append(parent1)
        offsprings.append(parent2)
        offsprings.append(offspring1)
        offsprings.append(offspring2)
    return offsprings


population = []
# initialize population with random strategies
for i in range(20):
    population.append(get_strategy_str(do_random))
# Iterate over cycles
for i in range(1000):
    population = play_a_cycle(population)

# for strat_str in population:
#     print(sum(1 if i else 0 for i in strat_str))
