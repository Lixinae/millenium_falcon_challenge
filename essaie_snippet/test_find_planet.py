##planets = [
##    {
##        "planet": "Tatooine",
##        "visited": False,
##        "reachable": ["Dagobah", "Hoth"]
##    },
##    {
##        "planet": "Dagobah",
##        "visited": False,
##        "reachable": ["Hoth", "Endor"]
##    },
##    {
##        "planet": "Endor",
##        "visited": False,
##        "reachable": []
##    },
##    {
##        "planet": "Hoth",
##        "visited": False,
##        "reachable": ["Endor"]
##    },
##]
##
##def build_reachables(planets, reachables):
##    reachable_planets = []
##    for planet in planets:
##        if planet["planet"] in reachables:
##            reachable_planets.append(planet)
##    return reachable_planets
##
##def explore_all_routes(planets, current_planet,trajectory):
##    current_planet["visited"] = True
##    print(current_planet)
##    trajectory.append(current_planet)
##    reachables = current_planet["reachable"]
##    reachables_list = build_reachables(planets,reachables)
##    for voisin in reachables_list:
##        if not voisin["visited"]:
##            explore_all_routes(planets, voisin, trajectory)
##
##
##
##for planet in planets:
##    trajectory = []
##    if not planet["visited"]:
##        explore_all_routes(planets, planet, trajectory)
##    planets[planet]

mylist =[{'trajectory': ['Tatooine', 'Hoth', 'Endor'], 'total_time': 7, 'caught_proba': 0.19},
         {'trajectory': ['Tatooine', 'Hoth', 'Endor'], 'total_time': 7, 'caught_proba': 0.18},
         {'trajectory': ['Tatooine', 'Hoth', 'Endor'], 'total_time': 7, 'caught_proba': 0}
         ]

def take_caught_proba(elem):
    return elem["caught_proba"]
mylist.sort(key=take_caught_proba)

print(mylist[0])
