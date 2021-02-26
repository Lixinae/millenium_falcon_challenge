from itertools import combinations

test = ['Umbara', 'Polis Massa', 'Kashyyyk', 'Ojom',
        'Skako', 'Geonosis', 'Trandosha', 'Bestine IV',
        'Bespin', 'Tholoth', 'Kamino', 'Mirial', 'Chandrila',
        'Champala', 'Aleen Minor', 'Troiken', 'Saleucami', 'Tatooine']
print("Test len:" + str(len(test)))
som = 0
for i in range(7, 10):
    combinaisons_planets_refuel = combinations(test[:len(test) - 1], i)
    list_combinaisons_planets_refuel = list(combinaisons_planets_refuel)
    print(len(list_combinaisons_planets_refuel))
    som += len(list_combinaisons_planets_refuel)

for combi in  list_combinaisons_planets_refuel:
    print(combi)
print("Total possible trajectories: " + str(som))

# https://haltode.fr/algo/general/approche/dynamique.html
# 19448 -> Nb combinaisons pour ce set de test
# taille_combi = 7
# nb_combi = 19448
# non_calcule = -1
# caught_max = [[non_calcule]*taille_combi for i in range(nb_combi)]
# caught_max[nb_combi][taille_combi]
## Todo ->
#   def maximiser_caught(index_combi, caught_dispo):
#     if index_combi > nb_combi:
#         return 0
#     if caught_max[index_combi][caught_dispo] != non_calcule:
#         return caught_min[index_combi][caught_dispo]
## Todo -> Ici corriger
#     combi = ??? -> Prendre
#     prend_pas_combi = maximiser_caught(index_combi+1,caught_dispo)
#     if odds.poids <= caught_dispo:
#       prend_combi = combi.importance +
#                           maximiser_caught(index_combi+1, caught_dispo - combi.poids
#     else:
#       prend_caught = 0
#     caught_max[index_combi][caught_dispo] = max(prend_pas_odds, prend_odds)
#     Retourner caught_max[index_combi][caught_dispo]
##########################
# Recursif non dynamique #
##########################
# maximiser_importance(index_objet, poids_dispo):
#    Si index_objet > nb_objets
#       Retourner 0
#
#    prend_pas_objet = maximiser_importance(index_objet + 1, poids_dispo)
#    Si objet.poids <= poids_dispo
#       prend_objet =  objet.importance +
#                      maximiser_importance(index_objet + 1, poids_dispo - objet.poids)
#    Sinon
#       prend_objet = 0
#
#    Retourner max(prend_pas_objet, prend_objet)
#
#
# Afficher maximiser_importance(1, poids_max)

######################
# Recursif dynamique #
######################
# importance_max[nb_objets_max][poids_max] initialisé à PAS_CALCULÉ
#
# maximiser_importance(index_objet, poids_dispo):
#    Si index_objet > nb_objets
#       Retourner 0
#    Si importance_max[index_objet][poids_dispo] != PAS_CALCULÉ
#       Retourner importance_max[index_objet][poids_dispo]
#
#    prend_pas_objet = maximiser_importance(index_objet + 1, poids_dispo)
#    Si objet.poids <= poids_dispo
#       prend_objet =  objet.importance +
#                      maximiser_importance(index_objet + 1, poids_dispo - objet.poids)
#    Sinon
#       prend_objet = 0
#
#    importance_max[index_objet][poids_dispo] = max(prend_pas_objet, prend_objet)
#    Retourner importance_max[index_objet][poids_dispo]
#
# Afficher maximiser_importance(1, poids_max)

######################
# Iteratif dynamique #
######################
# importance_max[nb_objets][poids_max]
#
# maximiser_importance():
#    Pour chaque poids
#       importance_max[0][iPoids] = 0
#
#    Pour chaque objet
#       Pour chaque poids
#          prend_pas_objet = importance_max[iObjet - 1][iPoids]
#          Si objet.poids <= iPoids
#             prend_objet =  objet.importance +
#                            importance_max[iObjet - 1][iPoids - objet.poids]
#          Sinon
#             prend_objet = 0
#
#          importance_max[iObjet][iPoids] = max(prend_objet, prend_pas_objet)
#
#    Retourner importance_max[nb_objets][poids_max]
