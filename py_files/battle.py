from py_files.pokemon import Pokemon
from py_files.trainer import Trainer
from py_files.moves import Move
import random

class Battle:
    
    CRIT_RATE = 0.0625 # Need to find a way to avoid float errors
    # Only going to have one trainer going against another
    TRAINER_1_ACTIVE = list()
    TRAINER_2_ACTIVE = list()

    def __init__(self, trainer_1, trainer_2, battle_type = "single"):
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_type = battle_type

    def get_trainer_1(self):
        return self.trainer_1
    
    def get_trainer_2(self):
        return self.trainer_2

    def get_battle_type(self):
        return self.battle_type

    def battle_start(self):
        trainers = [self.trainer_1, self.trainer_2]
        active_pkmn = [self.TRAINER_1_ACTIVE, self.TRAINER_2_ACTIVE]
        print(f"Battle start between {self.trainer_1.get_name()} and {self.trainer_2.get_name()}")
        for (trainer, active) in zip(trainers, active_pkmn):
            print(f"{trainer.get_name()} sends out ", end = "")
            for i in range(len(active)):
                print(active[i].get_name())
                if i == 1:
                    print(f" & {active[i].get_name()}")
        print()
    
    def process_active_pkmn(self, trainer, active):
        default = 1
        selected = False
        if self.battle_type == "double":
            default = 2
            
        while len(active) < default:
            selected = False
            print(f"Select starting Pokemon for {trainer.get_name()}. Options:")
            trainer.print_team()
            pkmn = int(input())
            for mon in active:
                if trainer.get_team()[pkmn - 1].get_name() == mon.get_name():
                    print(f"{trainer.get_team()[pkmn - 1].get_name()} is already an active Pokemon. Select another Pokemon")
                    selected = True
                    break
            
            if selected:
                continue

            if pkmn > len(trainer.get_team()) or pkmn <= 0:
                print(f"{pkmn} is not a valid number. Try again")
                continue

            # Adding Pokemon to active Pokemon slot
            active.append(trainer.get_team()[pkmn - 1])
            print(f"{trainer.get_team()[pkmn - 1].get_name()} added to the active slot\n")
    
    def pokemon_selection(self):
        trainers = [self.trainer_1, self.trainer_2]
        active_pkmn = [self.TRAINER_1_ACTIVE, self.TRAINER_2_ACTIVE]
        print(self.battle_type == "single")
        if self.battle_type in ["single", "double"]:
            for (trainer, active) in zip(trainers, active_pkmn):
                self.process_active_pkmn(trainer, active)
                 
    def move_selections(self):
        # Pass output to calculation functions
        pass

    def calculating_move_order(self):
        # May need sub-functions
        pass

    def chance_of_landing(self, prob):
        # prob should be between 0 and 100, can also be used for accuracy checks
        pass

if __name__ == "__main__":
    pass