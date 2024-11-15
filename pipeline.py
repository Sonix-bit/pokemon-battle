import pandas as pd
import numpy as np
from py_files.pokemon import Pokemon
from py_files.moves import Move
from py_files.trainer import Trainer
import keyboard
from ast import literal_eval
import pygame

# Reading in data from files
pokemon_file = "pokemon-data.csv"
pokemon = pd.read_csv(f"./data_files/{pokemon_file}", sep = ";")
print(pokemon.head())

pokemon_moves = "metadata_pokemon_moves.csv"
moves = pd.read_csv(f"./data_files/{pokemon_moves}")
print(moves.head())

matchup_file = "type_chart.csv"
type_matchup = pd.read_csv(f"./data_files/{matchup_file}")
print(type_matchup.head())

# idx = pokemon.loc[pokemon["Name"] == "Pichu"].index.astype(int)
# print(list(pokemon["Moves"].iloc[idx])[0])
pokemon[['Moves']] = pokemon[['Moves']].applymap(literal_eval)
pokemon[['Types']] = pokemon[['Types']].applymap(literal_eval)

moves_dict = {}
# Converting Pokemon and Moves into objects -> Game
for index, row in moves.iterrows():
    # print(row["short_description"])
    if "no additional effect" in row["short_description"]: 
        moves_dict[row["name"]] = {
            "accuracy": row["accuracy"],
            "pp": row["pp"],
            "power": row["power"],
            "priority": row["priority"],
            "type": row["type"],
            "damage_class": row["damage_class"],
            "side_effects": row["short_description"] # Need to refine to allow for secondary effects
        }
     
print("Dictionary of moves: ", moves_dict) # Need to manage status moves
moves_dict = {k.lower(): v for k, v in moves_dict.items()}

# Create Moves and Pokemon classes just before battle starts (need a counter for PP and tracking)

# Create Trainer Classes
print("***Welcome to Pokemon Math: no EVs, no IVs, 100% luck and calculations***")
trainer1_name = str(input("Player 1's name: "))
trainer1 = Trainer(trainer1_name)
trainer2_name = str(input("Player 2's name: "))
trainer2 = Trainer(trainer2_name)

print("Players created successfully!")
print(f"Trainer 1's name is {trainer1.name}")
print(f"Trainer 2's name is {trainer2.name}")

pokemon["Name"] = pokemon["Name"].apply(str.lower)
list_of_pokemon = list(pokemon["Name"])
print(f"Name of Pokemon: {list_of_pokemon}")

"""
Put this in a function
"""

print(f"Player 1 ({trainer1.name}): Choose your Pokemon (maximum 6)")

finalised = False # can add in confirmation flag later

def select_moveset(curr_mon, pokemon: pd.DataFrame):
    moveset = list()
    idx = pokemon.loc[pokemon["Name"] == curr_mon].index.astype(int)[0]
    # print(idx)
    pokemon_moveset = list(set([x.lower() for x in pokemon["Moves"][idx]]) & set(moves_dict.keys()))
    print(f"{curr_mon}'s moveset: {pokemon_moveset}")
    # Need to add additional condition if Pokemon only learns < 4 moves
    while len(moveset) < 4:
        if len(pokemon_moveset) == 0:
            print(f"{curr_mon} has no moves. Cannot be added to the team")
            break

        if len(moveset) == len(pokemon_moveset):
            print(f"No more valid moves can be added for {curr_mon}")
            break

        curr_move = str(input(f"Select moveset for {curr_mon} (4 moves). Press m for the moveset list for {curr_mon}. "))

        if curr_move == "m":
            print(f"{curr_mon}'s list of moves: {pokemon_moveset}")
            continue

        if curr_move.lower() not in pokemon_moveset:
            print(f"{curr_move} not a valid move for {curr_mon}")
            continue
            
        print(f"Move selected: {curr_move.lower()}")
        
        curr_move = curr_move.lower()
        if curr_move in pokemon_moveset and curr_move not in moveset:
            moveset.append(curr_move)
            print(f"{curr_move} added successfully to the move list for {curr_mon}")
            print(f"Current moveset for {curr_mon}: {moveset}")
    
    return moveset

def select_pokemon(pokemon: pd.DataFrame):
    pokemon_selected = dict()
    while len(pokemon_selected) < 6:
        print(len(pokemon_selected))
        
        curr_mon = str(input("Enter name of Pokemon (Press p for list of pokemon): ")) # Gonna be easier to format with a GUI
        if curr_mon == "p":
            print(f"List of Pokemon: {list_of_pokemon}")
            continue

        if curr_mon.lower() not in list_of_pokemon:
            print(f"{curr_mon} is not a valid Pokemon. Select another Pokemon. ")
            continue
        
        moveset = select_moveset(curr_mon, pokemon)
        adding = True
        if len(moveset) == 0:
            adding = False
        
        if adding:
            pokemon_selected[curr_mon] = moveset
        else:
            print(f"Unable to add {curr_mon}")

        print("Current Pokemon & Movesets:", pokemon_selected)

    return pokemon_selected

def adding_pokemon_to_trainers(trainer: Trainer, pokemon_selected):
    for key, value in pokemon_selected.items():
        curr = pokemon.loc[pokemon["Name"] == key]
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

trainers = [trainer1, trainer2]
for trainer in trainers:
    pokemon_selected = select_pokemon(pokemon)
# Need to convert dictionary to Pokemon objects
    adding_pokemon_to_trainers(trainer, pokemon_selected)
    print_team(trainer)

# After Pokemon attached to player, select first Pokemon to enter battle (need to work on switching Pokemon)
# Stats reset when Pokemon is switched out
# Can choose lineup (start with single battles for now), 6 v 6
from py_files.battle import Battle

battle = Battle(trainer1, trainer2)
flag = False
print("Battle start: \n")
print(f"{trainer1.get_name()} sends out {trainer1.team[0].get_name()}\n")
print(f"{trainer2.get_name()} sends out {trainer2.team[0].get_name()}\n")
turn = 1
while not flag:
    print(f"Turn {turn}")
    flag = battle.battle_turn(trainer1.team[0], trainer2.team[0])
    print(trainer1.team[0].get_hp(), trainer2.team[0].get_hp())
    turn += 1