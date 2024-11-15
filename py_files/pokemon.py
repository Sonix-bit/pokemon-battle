from typing import Dict, Union, List
from pathlib import Path
from py_files.moves import Move

class Pokemon:

    """
    Pokemon Class containing name, trainer and stats (will add nature, abilities and items)
    """

    STATS = ["HP", "ATK", "DEF", "SPD"] # "SP ATK", "SP DEF"
    BUFFS = {
        "ATK": 1,
        "DEF": 1,
        "SP_ATK": 1,
        "SP_DEF": 1,
        "SPD": 1,
        "EVASION": 1,
        "STATUS": None
    } # Keeping track of debuffs [HP, ATK, DEF, SP_ATK, SP_DEF, SPD, EVASION, STATUS]

    def __init__(self, name, moves: List[str], stats: Dict = None):
        self.name = name
        self.stats = stats
        self.moves = moves
        
    # Private Methods

    # Public Methods
    def get_name(self):
        return self.name
    
    def get_hp(self):
        return self.stats["HP"]
    
    def get_atk(self):
        return self.stats["ATK"]
    
    def get_def(self):
        return self.stats["DEF"]
    
    def get_sp_atk(self):
        return self.stats["SP_ATK"]
    
    def get_sp_def(self):
        return self.stats["SP_DEF"]
    
    def get_spd(self):
        return self.stats["SPD"]
    
    def get_types(self):
        return self.stats["TYPES"]
    
    def get_moves(self):
        return self.moves

    def reduce_hp(self, damage):
        self.stats["HP"] -= damage
        if self.stats["HP"] <= 0:
            self.stats["HP"] = 0
        
        return self.stats["HP"]

    def is_fainted(self):
        if self.stats["HP"] <= 0:
            print(f"{self.name} has fainted")
            return True
        
        return False    