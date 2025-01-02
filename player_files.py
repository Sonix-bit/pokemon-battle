import yaml
from py_files.trainer import Trainer
import pandas as pd
from py_files.pokemon import Pokemon
from ast import literal_eval
import os

def adding_pokemon_to_trainers(trainer: Trainer, pokemon_selected):
    for key, value in pokemon_selected.items():
        curr = pokemon.loc[pokemon["Name"].str.lower() == key]
        # print(curr["Name"])
        # curr_moves = trainer_data["pokemon"][key]
        # print(f"{key}'s moveset: {curr_moves} {value}")
        stats = {
            "HP": curr["HP"].values[0],
            "ATK": curr["Attack"].values[0],
            "DEF": curr["Defense"].values[0],
            "SP_ATK": curr["Special Attack"].values[0],
            "SP_DEF": curr["Special Defense"].values[0],
            "SPD": curr["Speed"].values[0],
            "TYPES": curr["Types"].values[0]
        }
        # Need a function to create move objects for each Pokemon before assigning it to each Pokemon

        p = Pokemon(name = key, stats = stats, moves = value)
        trainer.add_pokemon(p)

    return trainer

def print_team(trainer: Trainer):
    for mon in trainer.get_team():
        print("Name:", mon.get_name())
        print("HP:", mon.get_hp())
        print("Attack:", mon.get_atk())
        print("Defense:", mon.get_def())
        print("Special Attack:", mon.get_sp_atk())
        print("Special Defense:", mon.get_sp_def())
        print("Speed:", mon.get_spd())
        print("Types:", mon.get_types())

def create_trainer(yaml_file):
    with open(os.path.join("trainers", yaml_file)) as stream:
        trainer_data = yaml.safe_load(stream)

    # Creating trainer object
    trainer = Trainer(trainer_data["name"])
    pokemon_selected = trainer_data["pokemon"]
    print(pokemon_selected)
    trainer = adding_pokemon_to_trainers(trainer, pokemon_selected)
    print_team(trainer)
    return trainer

if __name__ == "__main__":

    ash_file = "ash.yaml"
    alain_file = "alain.yaml"

    # Reading in data from files
    pokemon_file = "pokemon_subset.csv"
    pokemon_path = os.path.join("data_files_subset", pokemon_file)
    pokemon = pd.read_csv(pokemon_path, sep = ";")

    pokemon[['Moves']] = pokemon[['Moves']].applymap(literal_eval)
    pokemon[['Types']] = pokemon[['Types']].applymap(literal_eval)

    ash = create_trainer(ash_file)
    alain = create_trainer(alain_file)

    print(ash.get_name())
    for p in ash.get_team():
        print(p.get_name(), p.get_moves(), p.get_img())
        print(p.create_move_list())

    print(alain.get_name())
    for p in alain.get_team():
        print(p.get_name(), p.get_moves(), p.get_img())
        print(p.create_move_list())

    # Create Move Objects for each pokemon in each team?? 

    # # Reading in YAML file
    # with open(os.path.join("trainers", ash_file)) as stream:
    #     trainer1_data = yaml.safe_load(stream)
        
    # print(trainer1_data)
    # # Creating trainer object
    # trainer1 = Trainer(trainer1_data["name"])

    # Reading in YAML file
    # with open(os.path.join("trainers", alain_file)) as stream:
    #     trainer2_data = yaml.safe_load(stream)
        
    # print(trainer2_data)
    # # Creating trainer object
    # trainer2 = Trainer(trainer2_data["name"])

    # trainers = [trainer1, trainer2]
    # for trainer in trainers:
        # pokemon_selected = trainer1_data["pokemon"]
        # # print(pokemon_selected)
        # # Need to convert dictionary to Pokemon objects
        # adding_pokemon_to_trainers(trainer, pokemon_selected)
        # print_team(trainer)