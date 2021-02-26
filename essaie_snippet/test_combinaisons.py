from itertools import combinations
test =['Umbara', 'Polis Massa', 'Kashyyyk', 'Ojom',
       'Skako', 'Geonosis', 'Trandosha', 'Bestine IV',
       'Bespin', 'Tholoth', 'Kamino', 'Mirial', 'Chandrila',
       'Champala', 'Aleen Minor', 'Troiken', 'Saleucami', 'Tatooine']
print("Test len:"+str(len(test)))
som = 0
for i in range(7,10):
    combinaisons_planets_refuel = combinations(test[:len(test) - 1], i)
    list_combinaisons_planets_refuel = list(combinaisons_planets_refuel)
    print("---------")
    print(len(list_combinaisons_planets_refuel))
    print(len(list_combinaisons_planets_refuel) / i)
    som += len(list_combinaisons_planets_refuel)

print("Total possible trajectories: " + str(som))


def caught_probability(count_time_encounter_bounty_hunters):
    caught_proba = 0
    for i in range(0, count_time_encounter_bounty_hunters):
        num = pow(9, i)
        denom = pow(10, i + 1)
        caught_proba += num / denom
    return caught_proba

n = 10
import time
start = time.time()
x = [caught_probability(x) for x in range(0, n)]
#caught_probability(n)
end = time.time()

print((end-start))
print((1-caught_probability(n))*100)
