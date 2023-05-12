import json
import requests
import random

API = "https://pokeapi.co/api/v2/pokemon/"

# api requests
def make_api_request(API):
    response = requests.get(API)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        return None

def make_limited_api_request(url, limit):
    endpoint = f"{url}?limit={limit}"
    data = make_api_request(endpoint)
    if data:
        return data
    else:
        return None


def get_pokemon_data(pokemon_name):
    endpoint = f"{API}{pokemon_name}"
    response = requests.get(endpoint)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Could not retrieve data for {pokemon_name.capitalize()}.")
        return None

#---------------------------------------------------------------------------------------------
#
def fetch_data(pokemon_name):
    endpoint = f"{API}{pokemon_name}"
    print(endpoint)
    pokemon_data = make_api_request(endpoint)
    hp = pokemon_data['stats'][0]['base_stat']
    weight = pokemon_data['weight']
    print(f"I choose {pokemon_name.capitalize()}. Its HP is {hp} and its weight is {weight}.")


def count_the_pokemon():
    endpoint = f"{API}?limit=1"
    pokemon_data = make_api_request(endpoint)
    count = pokemon_data['count']
    print(f"There are {count} pokemons.")

def get_weight_comparison_pokemon(pokemon_name):
    endpoint = f"{API}{pokemon_name}"
    pokemon_data = make_api_request(endpoint)
    pokemon_weight = pokemon_data['weight']
    endpoint = f"{API}?limit=50"
    pokemon_list = make_api_request(endpoint)['results']
    heavier_pokemon = []
    lighter_pokemon = []
    for p in pokemon_list:
        p_data = make_api_request(p['url'])
        if p_data['weight'] > pokemon_weight:
            heavier_pokemon.append(p['name'])
        elif p_data['weight'] < pokemon_weight:
            lighter_pokemon.append(p['name'])
    print(
        f"There are {len(heavier_pokemon)} pokemons heavier than {pokemon_name.capitalize()}: {', '.join(heavier_pokemon)}")
    print(
        f"There are {len(lighter_pokemon)} pokemons lighter than {pokemon_name.capitalize()}: {', '.join(lighter_pokemon)}")



def compare_pokemon_skill(pokemon_name, limit):
    endpoint = f"{API}{pokemon_name}"
    pokemon_data = make_api_request(endpoint)
    abilities = pokemon_data['abilities']
    print(f"The abilities of {pokemon_name.capitalize()} are:")
    for ability in abilities:
        print(f"- {ability['ability']['name'].capitalize()}")
    pokemon_ability = pokemon_data['abilities'][0]['ability']['name']
    endpoint = f"{API}?limit={limit}"
    pokemon_list = make_api_request(endpoint)['results']
    pokemon_with_same_ability = []
    for p in pokemon_list:
        p_data = make_api_request(p['url'])
        if pokemon_ability in [a['ability']['name'] for a in p_data['abilities']]:
            pokemon_with_same_ability.append(p['name'])
    print(f"There are {len(pokemon_with_same_ability)} pokemons with the same ability as {pokemon_name.capitalize()}: {', '.join(pokemon_with_same_ability)}")

def get_pokemon_moves(pokemon_name):
    endpoint = f"{API}{pokemon_name}"
    pokemon_data = make_api_request(endpoint)
    moves = []
    for move in pokemon_data['moves']:
        moves.append(move['move']['name'])
    print(f"{pokemon_name.capitalize()}'s moves are: {', '.join(moves)}")
    return moves


def get_pokemon_evolution(pokemon_data, pokemon_name):
    if 'evolution_chain' not in pokemon_data:
        return None

    chain_data = make_api_request(pokemon_data['evolution_chain']['url'])
    chain = chain_data['chain']

    def find_evolution(chain_link):
        if chain_link['species']['name'] == pokemon_name:
            if chain_link['evolves_to']:
                evolutions = []
                for evolution in chain_link['evolves_to']:
                    evolutions.append(evolution['species'][ 'name'])
                return evolutions
        elif chain_link['evolves_to']:
            for evolution in chain_link['evolves_to']:
                next_evolution = find_evolution(evolution)
                if next_evolution is not None:
                    return next_evolution
        return None

    try:
        evolutions = find_evolution(chain)
    except (KeyError, TypeError) as e:
        return []

    return evolutions if evolutions else []

def get_pokemon_stats(pokemon_name):
    API = "https://pokeapi.co/api/v2/pokemon/"
    endpoint = f"{API}{pokemon_name}"
    pokemon_data = make_api_request(endpoint)
    return pokemon_data['stats']

def print_stats(pokemon_name, stats):
    print(f"\nStats for {pokemon_name.capitalize()}:")

    for stat in stats:
        stat_name = stat['stat']['name']
        base_stat = stat['base_stat']
        print(f"{stat_name.capitalize()}: {base_stat}")


def show_evolution_benefits():
    API = "https://pokeapi.co/api/v2/pokemon-species/"
    pokemon_name = input("Enter the name of the Pokémon: ")
    endpoint = f"{API}{pokemon_name}"
    pokemon_data = make_api_request(endpoint)

    print(f"Stats for {pokemon_name}:")
    print_stats(pokemon_name, get_pokemon_stats(pokemon_name))

    evolutions = get_pokemon_evolution(pokemon_data, pokemon_name)
    if evolutions:
        for evolution in evolutions:
            print(f"Stats for {evolution}:")
            print_stats(evolution, get_pokemon_stats(evolution))
    else:
        print(f"{pokemon_name} has no evolutions.")


#mas coas

def show_all_data():
    pokemon_name = input("Enter the name of the Pokémon: ")

    fetch_data(pokemon_name)
    count_the_pokemon()
    get_weight_comparison_pokemon(pokemon_name)
    compare_pokemon_skill(pokemon_name, limit=100)
    get_pokemon_moves(pokemon_name)
    # Agrega las funciones para las características restantes aquí



#ALl Fight--------














POKEMON_API_BASE_URL = "https://pokeapi.co/api/v2/"
MOVE_API_ENDPOINT = "move/{move_name}"
POKEMON_API_ENDPOINT = "pokemon/{pokemon_name}"


def retrieve_data(endpoint):
    url = f"{POKEMON_API_BASE_URL}{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: Could not retrieve data for {endpoint.split('/')[-1]}.")


def get_move_power(move_name):
    endpoint = MOVE_API_ENDPOINT.format(move_name=move_name)
    data = retrieve_data(endpoint)
    if data:
        power = data['power']
        if power is None:
            print(f"{move_name.capitalize()} has no power, it does nothing.")
        return power


def get_pokemon_move(pokemon_name):
    endpoint = POKEMON_API_ENDPOINT.format(pokemon_name=pokemon_name)
    data = retrieve_data(endpoint)
    if data:
        moves_data = data['moves']
        moves = []
        for move_data in moves_data:
            moves.append(move_data['move']['name'])
        return moves


def get_base_health(pokemon_data):
    hp = pokemon_data['stats'][0]['base_stat']
    return hp


def simulate_fight():
    pokemon1_name = input("Enter the name of the first pokemon: ")
    pokemon2_name = input("Enter the name of the second pokemon: ")
    pokemon1_data = retrieve_data(POKEMON_API_ENDPOINT.format(pokemon_name=pokemon1_name))
    pokemon2_data = retrieve_data(POKEMON_API_ENDPOINT.format(pokemon_name=pokemon2_name))
    if not pokemon1_data or not pokemon2_data:
        return
    pokemon1_health = get_base_health(pokemon1_data)
    pokemon2_health = get_base_health(pokemon2_data)

    print(f"{pokemon1_name.capitalize()}'s moves are: {', '.join(get_pokemon_move(pokemon1_name))}")
    print(f"{pokemon2_name.capitalize()}'s moves are: {', '.join(get_pokemon_move(pokemon2_name))}")

    while pokemon1_health > 0 and pokemon2_health > 0:
        pokemon1_move = input(f"What move should {pokemon1_name.capitalize()} use? ")
        pokemon2_move = random.choice(get_pokemon_move(pokemon2_name))

        print(f"{pokemon1_name.capitalize()} attacks {pokemon2_name.capitalize()} with {pokemon1_move.capitalize()}.")
        pokemon1_move_power = get_move_power(pokemon1_move)
        if pokemon1_move_power:
            damage = calculate_damage(pokemon1_data, pokemon2_data, pokemon1_move_power)
            pokemon2_health -= damage
            print(f"It does {damage} damage.")
        else:
            continue

        if pokemon2_health <= 0:
            break

        print(f"{pokemon2_name.capitalize()} attacks {pokemon1_name.capitalize()} with {pokemon2_move.capitalize()}.")
        pokemon2_move_power = get_move_power(pokemon2_move)
        if pokemon2_move_power:
            damage = calculate_damage(pokemon2_data, pokemon1_data, pokemon2_move_power)
            pokemon1_health -= damage
            print(f"It does {damage} damage.")
        else:
            continue

        print(f"{pokemon1_name.capitalize()}'s health: {pokemon1_health}")
        print(f"{pokemon2_name.capitalize()}'s health: {pokemon2_health}")

    if pokemon1_health > 0:
        print(f"{pokemon1_name.capitalize()} wins!")
    else:
        print(f"{pokemon2_name.capitalize()} wins!")

def calculate_damage(attacker_data, defender_data, move_power):
    attacker_level = 50  # Assuming level 50 for simplicity
    attacker_attack = attacker_data['stats'][4]['base_stat']
    defender_defense = defender_data['stats'][3]['base_stat']
    modifier = 1  # For simplicity, we are not considering other factors like type effectiveness

    damage = ((((2 * attacker_level / 5) + 2) * move_power * (attacker_attack / defender_defense)) / 50 + 2) * modifier
    return int(damage)







def main():
    while True:
        print("--------------------------------------------------------")
        print("\nWhat do you want to know about Pokémon?")
        print("1. Fetch Pokémon Data")
        print("2. Count Pokémon")
        print("3. List Pokémon heavier than a certain weight")
        print("4. List Skills ans Pokémons with the same ability")
        print("5. List Pokémon moves")
        print("6. Show Pokemon Evolution")
        print("7. Show Pokemon Evolution Benefits")
        print("8. Show all Pokémon data")
        print("9. Fight 2 Pokemons")
        print("0. Exit")

        choice = input("Enter your choice (0-9): ")

        if choice == "1":
            pokemon_name = input("Enter the name of the Pokémon: ")
            fetch_data(pokemon_name)
        elif choice == "2":
            count_the_pokemon()
        elif choice == "3":
            pokemon_name = input("Enter the name of the Pokémon: ")
            get_weight_comparison_pokemon(pokemon_name)
        elif choice == "4":
            pokemon_name = input("Enter the name of the Pokémon: ")
            compare_pokemon_skill(pokemon_name, limit=50)

        elif choice == "5":
            pokemon_name = input("Enter the name of the pokemon: ")
            get_pokemon_moves(pokemon_name)

        elif choice == "6":
            API = "https://pokeapi.co/api/v2/pokemon-species/"
            pokemon_name = input("Enter the name of the Pokémon: ")
            endpoint = f"{API}{pokemon_name}"
            pokemon_data = make_api_request(endpoint)
            print(get_pokemon_evolution(pokemon_data, pokemon_name))
            get_pokemon_evolution(pokemon_name, pokemon_data)




        elif choice== "7":
            pokemon_name = input("Enter the Name of The pokemon: ")
            show_evolution_benefits()

        elif choice == "8":
            show_all_data()
        elif choice == "9":
            simulate_fight()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


