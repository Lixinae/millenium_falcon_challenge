# Todo -> Réécrire combinationsde itertools
#  Pour ajouter pour chaque combinaison le poids de capture
#  (Pour n'écrire qu'une seule fois les calculs et éviter de réiterer sur
#  quelques chose où j'ai déjà itérer

def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    """
    Return r length subsequences of elements from the input iterable.

    The combination tuples are emitted in lexicographic
    ordering according to the order of the input iterable.
    So, if the input iterable is sorted,
    the combination tuples will be produced in sorted order.
    Elements are treated as unique based on their position, not on their value. So if the input elements are unique, there will be no repeat values in each combination.
    """
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = [x for x in range(r)]
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        yield tuple(pool[i] for i in indices)


# print(len(list(combinations(test[:len(test) - 1],7))))

def combinations_no_yield(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    """
    Return r length subsequences of elements from the input iterable.

    The combination tuples are emitted in lexicographic
    ordering according to the order of the input iterable.
    So, if the input iterable is sorted,
    the combination tuples will be produced in sorted order.
    Elements are treated as unique based on their position, not on their value. So if the input elements are unique, there will be no repeat values in each combination.
    """
    result = []
    pool = tuple(iterable)
    print(pool)
    n = len(pool)
    if r > n:
        return
    indices = [x for x in range(r)]

    result.append(tuple(pool[i] for i in indices))
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return result
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        result.append(tuple(pool[i] for i in indices))


def combinations_falcon_data(trajectory,
                             taille_combi,
                             bounty_hunters,
                             caught_probability_values,
                             autonomy,
                             empire_countdown,
                             json_database):
    result = []
    pool = tuple(trajectory)
    n = len(pool)
    if taille_combi > n:
        return
    indices = [x for x in range(taille_combi)]

    # Todo -> Ici calculer la distance total
    # Les refuels, les proba d'être capturé etc...
    # Si la combinaison depasse le temps de trajet -> On ajoute pas le tuple
    combinaison = tuple(pool[i] for i in indices)
    data = calculate_total_time_odds_for_combinaison(combinaison,
                                                     bounty_hunters,
                                                     caught_probability_values,
                                                     autonomy,
                                                     empire_countdown,
                                                     json_database,
                                                     trajectory)
    # Data looks like
    # {
    #     "trajectory": trajectory,
    #     "total_time": total_travel_time_with_refuel,
    #     "caught_proba": caught_proba,
    #     "refueled_on": refueled_on
    # }

    if data["total_time"] <= empire_countdown:
        result.append(data)
    while True:
        for i in reversed(range(taille_combi)):
            if indices[i] != i + n - taille_combi:
                break
        else:
            return result
        indices[i] += 1
        for j in range(i + 1, taille_combi):
            indices[j] = indices[j - 1] + 1
        combinaison = tuple(pool[i] for i in indices)
        data = calculate_total_time_odds_for_combinaison(combinaison,
                                                         bounty_hunters,
                                                         caught_probability_values,
                                                         autonomy,
                                                         empire_countdown,
                                                         json_database,
                                                         trajectory)
        if data["total_time"] <= empire_countdown:
            result.append(data)


test = ['Umbara', 'Polis Massa', 'Kashyyyk', 'Ojom',
        'Skako', 'Geonosis', 'Trandosha', 'Bestine IV',
        'Bespin', 'Tholoth', 'Kamino', 'Mirial', 'Chandrila',
        'Champala', 'Aleen Minor', 'Troiken', 'Saleucami', 'Tatooine']

test = ['a', 'b', 'c', 'd', 'e', 'f', 'g', ]

combi = combinations_falcon_data(test[:len(test) - 1], 3)
print(len(combi))
# print(combi)
