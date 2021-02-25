from backend_millenium_falcon_computer.mass_data_generator.empire_data_generator import generate_empire_data
from backend_millenium_falcon_computer.mass_data_generator.millenium_falcon_generator import generate_falcon_data
from backend_millenium_falcon_computer.mass_data_generator.planets_data_generator import generate_planets_data

generate_planets_parameters = {
    "number_planets": 100,
    "min_destinations": 1,
    "max_destinations": 5,
    "min_travel_time": 1,
    "max_travel_time": 8
}
generated_planets = generate_planets_data(generate_planets_parameters)

if __name__ == '__main__':
    generate_planets_parameters = {
        "number_planets": 50,
        "min_destinations": 1,
        "max_destinations": 5,
        "min_travel_time": 1,
        "max_travel_time": 8
    }
    generated_planets = generate_planets_data(generate_planets_parameters)

    numb_of_bounty_hunters = 50
    generated_empire = generate_empire_data(numb_of_bounty_hunters)

    generated_falcon = generate_falcon_data()
