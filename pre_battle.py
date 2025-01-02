import pandas as pd
import numpy as np
from py_files.pokemon import Pokemon
from py_files.moves import Move
from py_files.trainer import Trainer
from ast import literal_eval
import os
import yaml
from py_files.battle import Battle

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

    # Creating Trainer object
    trainer = Trainer(trainer_data["name"])
    pokemon_selected = trainer_data["pokemon"]
    print(pokemon_selected)
    trainer = adding_pokemon_to_trainers(trainer, pokemon_selected)
    print_team(trainer)
    return trainer

def reading_csv_files(pokemon_file, pokemon_moves, matchup_file):
    # Reading in data from files
    pokemon = pd.read_csv(os.path.join("data_files_subset", pokemon_file), sep = ";")
    moves = pd.read_csv(os.path.join("data_files_subset", pokemon_moves), index_col = 'name')
    type_matchup = pd.read_csv(os.path.join("data_files_subset", matchup_file), index_col = "Attacking")

    pokemon[['Moves']] = pokemon[['Moves']].applymap(literal_eval)
    pokemon[['Types']] = pokemon[['Types']].applymap(literal_eval)
    return pokemon, moves, type_matchup

def process_moves(moves):
    moves_dict = {}
    # Converting Pokemon and Moves into objects -> Game
    for index, row in moves.iterrows():
        print(index)
        moves_dict[index] = {
            "name": index,
            "accuracy": row["accuracy"],
            "pp": row["pp"],
            "power": row["power"],
            "priority": row["priority"],
            "type": row["type"],
            "damage_class": row["damage_class"],
            "description": row["short_description"],
            "stat_change": str(row["stat_change"]).split(","),
            "status_change": row["status_change"],
            "chance": row["chance"],
            "target": row["target"] # Need to refine to allow for secondary effects
        }

    for index, row in moves.iterrows():
        # print(len(moves_dict[row["name"]]["stat_change"]))
        if len(moves_dict[index]["stat_change"]) > 1:
            moves_dict[index]["stat_change"][1] = float(moves_dict[index]["stat_change"][1])

    # print("Dictionary of moves: ", moves_dict) # Need to manage status moves
    moves_dict = {k.lower(): v for k, v in moves_dict.items()}
    print("Dictionary of moves: ", moves_dict) # Need to manage status moves
    return moves_dict

if __name__ == "__main__":
    # Reading in files
    pokemon_file = "pokemon_subset.csv"
    pokemon_moves = "pokemon_moves.csv"
    matchup_file = "type_chart.csv"

    pokemon, moves, type_matchup = reading_csv_files(pokemon_file, pokemon_moves, matchup_file)
    moves_dict = process_moves(moves)
    print(moves_dict)

    # Read in YAML files
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

    # Battle Time
    """
    1. Create Battle Object (Pass through Trainers)
    2. Trainers select their lineup (2 Pokemon to lead)
    3. Battle Start - Player 1 selects moves, Player 2 selects moves
    4. Back end functions returning what info needs to be updated and turn order
        a. Switches -> Priority moves -> Speed -> Tiebreak
    5. Update dialogue and info (HP bar changes)
        a. Switch Pokemon in if fainted
    6. Move turn += 1 (check if an opponent has won)
    """
    battle = Battle(ash, alain)
    battle.pokemon_selection()
    battle.battle_start()
    counter = 1
    while battle.TRAINER_1_ACTIVE == 0 or battle.TRAINER_2_ACTIVE == 0:
        print(f"------ Turn {counter} ------")
        
        counter += 1