    for combinaisons_planet_refuel in list_combinaisons_planets_refuel:
        # A partir du moment où on a une probabilité à 0 pour un trajet, on ne pourra pas avoir mieux
        if any([x for x in trajectories_time_and_caught_proba if x["caught_proba"] == 0]):
            return find_best_proba_success(trajectories_time_and_caught_proba)

        total_travel_time_with_refuel = 0
        count_time_encounter_bounty_hunters = 0
        current_fuel = autonomy
        refueled_on = []
        for i in range(0, len(trajectory) - 1):
            travel_between = get_travel_time_between(trajectory[i], trajectory[i + 1], json_database)
            current_planet = {
                "planet": trajectory[i],
                "day": total_travel_time_with_refuel
            }
            if current_planet in bounty_hunters:
                count_time_encounter_bounty_hunters += 1
            for planet in combinaisons_planet_refuel:
                if current_planet["planet"] == planet:
                    refueled_on.append(planet)
                    total_travel_time_with_refuel += 1
                    current_planet["day"] = total_travel_time_with_refuel
                    current_fuel = autonomy
                    if current_planet in bounty_hunters:
                        count_time_encounter_bounty_hunters += 1

            predicted_fuel = current_fuel - travel_between
            if predicted_fuel < 0:  # On a besoin de refuel
                total_travel_time_with_refuel += 1
                current_planet["day"] = total_travel_time_with_refuel
                current_fuel = autonomy
                refueled_on.append(current_planet["planet"])
                if current_planet in bounty_hunters:
                    count_time_encounter_bounty_hunters += 1
            current_fuel -= travel_between
            total_travel_time_with_refuel += travel_between
        if count_time_encounter_bounty_hunters > len(caught_probability_values):
            caught_proba = caught_probability(caught_probability_values)
        else:
            caught_proba = caught_probability_values[count_time_encounter_bounty_hunters]
        # Il est inutile de créer l'objet et de l'ajouter à la liste si on excède le temps
        if total_travel_time_with_refuel <= empire_countdown:
            trajectory_time_and_caught_proba = {
                "trajectory": trajectory,
                "total_time": total_travel_time_with_refuel,
                "caught_proba": caught_proba,
                "refueled_on": refueled_on
            }
            trajectories_time_and_caught_proba.append(trajectory_time_and_caught_proba)
