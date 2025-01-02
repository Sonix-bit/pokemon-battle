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
        self.name = self.move_info["name"]
        self.accuracy = float(self.move_info["accuracy"])
        self.pp = int(self.move_info["pp"])
        self.power = float(self.move_info["power"])
        self.priority = int(self.move_info["priority"])
        self.type = self.move_info["type"]
        self.desc = self.move_info["description"]
        self.damage_class = self.move_info["damage_class"]
        self.stat_changes = self.move_info["stat_change"]
        self.status_changes = self.move_info["status_change"]
        self.chance = int(self.move_info["chance"])
        self.target = self.move_info["target"]

    # Public methods
    def get_name(self):
        return self.name
    
    def get_accuracy(self):
        return self.accuracy
    
    def get_pp(self):
        return self.pp
    
    def get_power(self):
        return self.power
    
    def get_priority(self):
        return self.priority
    
    def get_movetype(self):
        return self.type 
    
    def get_desc(self):
        return self.desc
    
    def get_damage_class(self):
        return self.damage_class
    
    def get_stat_change(self):
        return self.stat_changes
    
    def get_status_change(self):
        return self.status_changes
    
    def get_chance(self):
        return self.chance
    
    def get_target(self):
        return self.target

    def reduce_pp(self):
        self.pp -= 1
        return self.pp

    def no_pp(self):
        if self.pp == 0:
            return "Cannot Use"
            
        elif self.pp > 0:
            return True

if __name__ == "__main__":
    pass
    # move_info = {
    #     "name": "Flame Charge",
    #     "type": "FIRE",
    #     "power": 40,
    #     "category": "physical",
    #     "side_effects": True,
    #     "stat_changes": ["SPD", "UP", 1],
    #     "target": "single" # Single, all, opponent
    # }

    # fc = Move(move_info)
    # print(fc.get_name())
