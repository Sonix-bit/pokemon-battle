import pandas as pd
import string

pokemon_moves = "metadata_pokemon_moves.csv"
moves = pd.read_csv(f"./files/{pokemon_moves}")
# print(moves.head())
damaging_moves = moves.loc[moves["damage_class"] != "Status"]
# print(set(damaging_moves["short_description"].str.lower().to_list()))

# Split lists into individual words and work from there
# Could focus only on physical and special moves to begin with
# Start with moves that have no side effects
regular_move = "no additional effect"
punc = '''!()-[]{};:'"\,<>./?@#$^&*_~'''
descriptions = damaging_moves["short_description"].str.lower().to_list()

move_names = []
for description in descriptions:
    translating = str.maketrans('', '', string.punctuation)
    new_string = description.translate(translating)
    # print(new_string)
    # print(regular_move in new_string)
    # if regular_move in new_string:
    #     move_names.append()
    # Need to determine if 

moves_dict = {}
# Converting Pokemon and Moves into objects -> Game
for index, row in moves.iterrows():
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

"""
Battle Mechanics
"""