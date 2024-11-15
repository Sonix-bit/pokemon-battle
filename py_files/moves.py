#!/bin/bash
from typing import Dict, Union, List

class Move:
    # Move name
    # Move type
    # Power
    # Physical/Special/Status
    # Extra side effects
    # Target

    def __init__(self, move_info: Dict):
        self.move_info = move_info

    # Public methods
    def get_name(self):
        return self.move_info["name"]
    
    def get_movetype(self):
        return self.move_info["type"] 
    
    def get_power(self):
        return self.move_info["power"]
    
    def get_category(self):
        return self.move_info["category"]
    
    def get_side_effects(self):
        return self.move_info["side_effects"]
    
    def stat_changes(self):
        return self.move_info["stat_changes"]
    
    def get_target(self):
        return self.move_info["target"]

if __name__ == "__main__":
    move_info = {
        "name": "Flame Charge",
        "type": "FIRE",
        "power": 40,
        "category": "physical",
        "side_effects": True,
        "stat_changes": ["SPD", "UP", 1],
        "target": "single" # Single, all, opponent
    }

    fc = Move(move_info)
    print(fc.get_name())
