from pokemon import Pokemon
from trainer import Trainer
from moves import Move
import random

class Battle:
    
    CRIT_RATE = 0.0625 # Need to find a way to avoid float errors

    WEAKNESSES = {
        "FIRE": ["GRASS", "ICE"],
        "WATER": ["FIRE", "ROCK"],
        "GRASS": ["WATER", "GROUND"]
    }

    RESISTANCES = {
        "WATER": ["FIRE"],
        "FIRE": ["GRASS"], 
        "GRASS": ["WATER"]
    }

    IMMUNITIES = {
        
    }

    def __init__(self, trainer_1, trainer_2):
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
    
    def calculate_damage(self, p1: Pokemon, p2: Pokemon):
        """
        Calculating the damage taken by each pokemon (min damage is 1)
        Will do the physical/special split

        """
        weakness_multiplier = 1
        STAB = 1.5
        crit_multiplier = False

        super_effective = False
        not_effective = False

        # Pokemon 1 is weak to Pokemon 2 type (will update to being move)
        if p2.get_type() in self.WEAKNESSES[p1.get_type()]:
            weakness_multiplier *= 2
        
        # Pokemon 2 resists pokemon 1's type (implement with coverage moves)
        if p1.get_type() in self.RESISTANCES[p2.get_type()]:
            weakness_multiplier /= 2.0

        if weakness_multiplier >= 2.0:
            super_effective = True

        elif weakness_multiplier <= 0.5:
            not_effective = True

        print(f"-----------------{p1.get_name()} damage multipliers---------------")
        print(f"Weakness multiplier: {weakness_multiplier}")
        rand = random.random()
        print("Random number for CRIT: ", rand)
        if rand < self.CRIT_RATE:
            weakness_multiplier *= 1.5
            crit_multiplier = True

        damage = (p1.get_atk() - p2.get_def()) * weakness_multiplier * crit_multiplier
        if damage <= 0:
            damage = 1

        p2.reduce_hp(damage)
        string = f"{p1.get_name()} has dealt {damage} damage."
        additional_str = ""
        if crit_multiplier:
            additional_str += " Critical hit!"
        if super_effective:
            additional_str += " It's super effective!"
        elif not_effective:
            additional_str += " It's not very effective!"

        print(string + additional_str)
        print(f"{p2.name} has {p2.get_hp()} HP left!\n")

    def faint_checks(self, p1: Pokemon, p2: Pokemon):
        
        self.calculate_damage(p2, p1)
        p1_fainted = p1.is_fainted()

        if p1_fainted:
            return p1_fainted

        self.calculate_damage(p1, p2)
        p2_fainted = p2.is_fainted()
        if p2_fainted:
            return p2_fainted
    
    # Need to code up battle priority
    def battle_turn(self, p1: Pokemon, p2: Pokemon):
        # Checking what move player wants to use
        for i, elem in enumerate(p1.get_moves()):
            print(f"{i}: {elem}")

        p1_input = input(f"What move should {p1.get_name()} do? (numeric input)")

        for i, elem in enumerate(p2.get_moves()):
            print(f"{i}: {elem}")

        p2_input = input(f"What move should {p2.get_name()} do? (numeric input)")
        # Check for status conditions (to be implemented later)

        # Compare speed of Pokemon
        faster = p1.get_spd() > p2.get_spd()
        slower = p1.get_spd() < p2.get_spd()
        
        if faster:
            faint_flag = self.faint_checks(p2, p1)
            if faint_flag:
                return faint_flag

        elif slower:
            faint_flag = self.faint_checks(p1, p2)
            if faint_flag:
                return faint_flag

        else:
            # Speed tie
            chance = random.random()
            if chance < 0.5:
                faint_flag = self.faint_checks(p1, p2)
                if faint_flag:
                    return faint_flag

            else:
                faint_flag = self.faint_checks(p2, p1)
                if faint_flag:
                    return faint_flag

        return False

if __name__ == "__main__":

    stats1 = {
        "HP": 100,
        "ATK": 60,
        "DEF": 40, 
        "SPD": 100, 
        "TYPE": "WATER"
    }

    flame_charge = {
        "name": "Flame Charge",
        "type": "FIRE",
        "power": 60,
        "category": "physical",
        "side_effects": True,
        "stat_changes": ["SPD", "UP", 1],
        "target": "single" # Single, all, opponent
    }

    bubblebeam = {
        "name": "Bubblebeam",
        "type": "WATER",
        "power": 65,
        "category": "special",
        "side_effects": True,
        "stat_changes": ["STATUS", True, "confusion"],
        "target": "single" # Single, all, opponent
    }

    fc = Move(flame_charge)
    bb = Move(bubblebeam)

    stats2 = {
        "HP": 100,
        "ATK": 60,
        "DEF": 40,
        "SPD": 101,
        "TYPE": "FIRE",
        "MOVES": [fc]
    }

    p1 = Pokemon("Squirtle", stats = stats1, moves = [bb])
    p2 = Pokemon("Charmander", stats = stats2, moves = [fc])
    ash = Trainer("Ash")
    alain = Trainer("Alain")
    
    ash.add_pokemon(p1)
    alain.add_pokemon(p2)

    print("Ash pokemon:", ash.team[0].name)
    print("Alain pokemon:", alain.team[0].name)

    battle = Battle(ash, alain)
    flag = False
    print("Battle start: \n")
    print(f"{ash.get_name()} sends out {ash.team[0].get_name()}\n")
    print(f"{alain.get_name()} sends out {alain.team[0].get_name()}\n")
    turn = 1
    while not flag:
        print(f"Turn {turn}")
        flag = battle.battle_turn(ash.team[0], alain.team[0])
        turn += 1

    print(ash.team[0].get_hp(), alain.team[0].get_hp())