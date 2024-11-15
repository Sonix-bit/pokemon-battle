import yaml
from trainer import Trainer
import pandas as pd
from pokemon import Pokemon
from ast import literal_eval

trainer1_file = "trainer1.yaml"
trainer2_file = "trainer2.yaml"

# Reading in data from files
pokemon_file = "pokemon-data.csv"
pokemon = pd.read_csv(f"./files/{pokemon_file}", sep = ";")
print(pokemon.head())
pokemon[['Moves']] = pokemon[['Moves']].applymap(literal_eval)
pokemon[['Types']] = pokemon[['Types']].applymap(literal_eval)

# Reading in YAML file
with open(f"trainers/{trainer1_file}") as stream:
    trainer1_data = yaml.safe_load(stream)
    
print(trainer1_data)
# Creating trainer object
trainer1 = Trainer(trainer1_data["name"])

def adding_pokemon_to_trainers(trainer: Trainer, pokemon_selected):
    for key, value in pokemon_selected.items():
        print(pokemon["Name"].str.lower() == "xatu")
        curr = pokemon.loc[pokemon["Name"].str.lower() == key]
        
        print(f"Current Pokemon: {curr}")
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

trainers = [trainer1]
for trainer in trainers:
    pokemon_selected = trainer1_data["pokemon"]
    # for pokemon_selected in trainer_mon:
    print(pokemon_selected)
    # Need to convert dictionary to Pokemon objects
    adding_pokemon_to_trainers(trainer, pokemon_selected)
    print_team(trainer)