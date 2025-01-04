from py_files.pokemon import Pokemon
from py_files.trainer import Trainer
from py_files.moves import Move
import random
import math

class Battle:
    
        # Only going to have one trainer going against another

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_type = "single"):
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_type = battle_type
        self.trainers = [self.trainer_1, self.trainer_2]
        self.TRAINER_1_ACTIVE = list()
        self.TRAINER_2_ACTIVE = list()
        self.active_pkmn = [self.TRAINER_1_ACTIVE, self.TRAINER_2_ACTIVE]
        
    def get_trainer_1(self):
        return self.trainer_1
    
    def get_trainer_2(self):
        return self.trainer_2

    def get_battle_type(self):
        return self.battle_type
    
    def get_trainers(self):
        return self.trainers

    def get_active_pkmn(self):
        return self.active_pkmn

    def get_trainer_1_active(self):
        return self.TRAINER_1_ACTIVE

    def get_trainer_2_active(self):
        return self.TRAINER_2_ACTIVE

    def battle_start(self):
        print(f"Battle start between {self.trainer_1.get_name()} and {self.trainer_2.get_name()}")
        for (trainer, active) in zip(self.trainers, self.active_pkmn):
            print(f"{trainer.get_name()} sends out ", end = "")
            for i in range(len(active)):
                print(active[i].get_name())
                if i == 1:
                    print(f" & {active[i].get_name()}")
        print()
    
    def process_active_pkmn(self, trainer, active):
        default = 1 # One v One Pokemon
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
        print(self.battle_type == "single")
        if self.battle_type in ["single", "double"]:
            for (trainer, active) in zip(self.trainers, self.active_pkmn):
                self.process_active_pkmn(trainer, active)

    def switch_selection(self, trainer, active_pkmn):
        # [Trainer name, Active Pokemon name, "switch", Pokemon in party, speed stat]
        # Difference between two lists
        chosen_moves = list()
        mon_switching_in = None
        for pkmn in active_pkmn:
            print("Pokemon in the back:")
            trainer_party = trainer.get_team()
            pkmn_in_party = [mon for mon in trainer_party if mon not in active_pkmn and mon.get_hp() > 0]

            if pkmn_in_party is None or len(pkmn_in_party) == 0:
                print("No Pokemon in the back. Select the battle option.")
                return

            for i, mon in enumerate(pkmn_in_party):
                print(f"{i + 1} - {mon.get_name()}")

            while True:
                # Retrieve Pokemon from list
                chosen_pkmn = int(input("Select Pokemon (numerical input): "))
                # Remove current Pokemon and add in new Pokemon (new function)
                if chosen_pkmn > len(pkmn_in_party) or chosen_pkmn <= 0:
                    print("Invalid Pokemon. Try again")
                    continue
                else:
                    mon_switching_in = pkmn_in_party[chosen_pkmn - 1]
                    print(f"{mon_switching_in.get_name()} selected to switch in next turn.")
                    break

            chosen_moves.append([trainer, 
                                 pkmn,
                                 "switch", 
                                 mon_switching_in, 
                                 int(pkmn.get_spd())]) 

        return chosen_moves

    def initial_options(self, trainer, active_pkmn):
        print(f"{trainer.get_name()}'s turn")
        chosen_option = list()
        # flag = True
        while True:
            print("Options:\n1 - Battle\n2 - Pokemon")
            option = int(input("Select option: "))
            # Move Selection option
            if option == 1:
                chosen_option = self.move_selection(trainer, active_pkmn)
                # Need to add option to struggle when pp hits zero on all moves
                break

            # Switch option
            elif option == 2:
                chosen_option = self.switch_selection(trainer, active_pkmn)
                if chosen_option is None:
                    print("Switch option invalid. Select Battle.")
                    continue

                break

            else:
                print("Invalid options. Try again")

        return chosen_option

    def move_selection(self, trainer, active_pkmn):
        # Pass output to calculation functions
        # [trainer name (assumes it's different), pokemon name, 'battle', move name, speed]
        chosen_moves = list()
        for pkmn in active_pkmn:
            while True:
                print(f"Select move for {pkmn.get_name()}")
                pkmn.print_moves()
                option = int(input())
                if option >= 1 and option <= 4: # Between 1 and 4
                    print(pkmn.get_moves()[option - 1])
                    break
                else:
                    print("Invalid move. Select a valid move")

            # Need to update for double battles
            chosen_moves.append([trainer, 
                                 pkmn,
                                 "battle", 
                                 pkmn.get_moves()[option - 1],
                                 int(pkmn.get_spd())])

        return chosen_moves

    def calculating_move_order(self, moves_for_turn):
        # May need sub-functions
        print(moves_for_turn)
        """
        Move Order
        1. Switch (check speed tie)
        2. Normal moves (check speed tie)
        """
        # move_order = dict()
        # max_switch_speed = None # Need to modify for double battle
        switch_moves = list()
        battle_moves = list()
        for turns in moves_for_turn:
            
            # Can only either be switching or battling
            if turns[2] == "switch":
                switch_moves.append(turns)
            
            else:
                battle_moves.append(turns)

        print(f"Switch moves: {switch_moves}")
        print(f"Battle moves: {battle_moves}")

        switch_moves_sorted = sorted(switch_moves,key=lambda l: (l[4], l[4] - random.random()), reverse=True)
        battle_moves_sorted = sorted(battle_moves,key=lambda l: (l[4], l[4] - random.random()), reverse=True)

        print(f"Switch moves sorted: {switch_moves_sorted}")
        print(f"Battle moves sorted: {battle_moves_sorted}")
        return switch_moves_sorted, battle_moves_sorted

    def chance_of_landing(self, prob) -> bool: 
        # prob should be between 0 and 100, can also be used for accuracy checks
        rand = random.random() * 100
        if rand >= prob: # If prob is in rand
            return False
        
        return True
    
    def swap_active_pkmn(self, switches, ACTIVE_PKMN, trainer: Trainer):
        print(f"{switches[1].get_name()} belongs to {trainer.get_name()}")
        ACTIVE_PKMN.append(switches[3]) # Add Pokemon to switch in
        ACTIVE_PKMN.remove(switches[1]) # Remove Active Pokemon (should work for double battles)
        print(f"{switches[1].get_name()} come back! {trainer.get_name()} sends out {switches[3].get_name()}")
        return ACTIVE_PKMN
    
    def process_switch(self, switch_moves):
        # If there are no switch moves, return from the function
        if switch_moves is None or len(switch_moves) == 0:
            return
        
        # Process switches, updating the active Pokemon and party slots
        for switches in switch_moves:
            if switches[0] == self.get_trainer_1():
                # self.TRAINER_1_ACTIVE
                self.TRAINER_1_ACTIVE = self.swap_active_pkmn(switches, self.TRAINER_1_ACTIVE, self.get_trainer_1())

            else:
                # self.TRAINER_2_ACTIVE
                self.TRAINER_2_ACTIVE = self.swap_active_pkmn(switches, self.TRAINER_2_ACTIVE, self.get_trainer_2())

    def process_battle_move(self, battle_moves, moves_dict, type_matchup):

        if len(battle_moves) == 0:
            return
        
        damage_divider = 5
        crit_rate = 0.0625

        # [trainer name, pokemon name, 'battle', move name, speed]
        for battles in battle_moves:
            crit_statement = ""
            crit_damage = 1
            STAB = 1

            if battles[0] == self.get_trainer_1():
                # self.TRAINER_1_ACTIVE attacking self.TRAINER_2_ACTIVE slot
                opposing_pkmn = self.get_trainer_2_active()[0] # May update for double battle
                is_crit = crit_rate >= random.random()
                is_landing = self.chance_of_landing(int(moves_dict[battles[3]]['accuracy']))
                if not is_landing:
                    print(f"{battles[1].get_name()} used {battles[3]}. {opposing_pkmn.get_name()} avoided the attack.")
                    continue

                # print("Is crit", is_crit)
                if is_crit:
                    crit_damage = 1.5
                    crit_statement = " It's a critical hit!"
                
                effectiveness, STAB = self.effectiveness_calculations(battles, moves_dict, type_matchup, opposing_pkmn)

                if moves_dict[battles[3]]['damage_class'].lower() == "physical":
                    outcome = self.physical_special_splits(
                        "physical", battles[1], opposing_pkmn, STAB, moves_dict, battles, \
                        effectiveness, crit_damage, damage_divider, self.get_trainer_2(), self.TRAINER_2_ACTIVE, crit_statement)
                    if outcome == "Done":
                        return

                elif moves_dict[battles[3]]['damage_class'].lower() == "special":
                    outcome = self.physical_special_splits(
                        "special", battles[1], opposing_pkmn, STAB, moves_dict, battles, \
                        effectiveness, crit_damage, damage_divider, self.get_trainer_2(), self.TRAINER_2_ACTIVE, crit_statement)
                    if outcome == "Done":
                        return
                # Add calculation damages to opposing Pokemon
                # Check if Pokemon is fainted (if so, then remove from opponent's party)
            
            else:
                # self.TRAINER_2_ACTIVE attacking self.TRAINER_1_ACTIVE slot
                opposing_pkmn = self.get_trainer_1_active()[0] # May update for double battle
                is_crit = crit_rate >= random.random()
                is_landing = self.chance_of_landing(int(moves_dict[battles[3]]['accuracy']))
                if not is_landing:
                    print(f"{battles[1].get_name()} used {battles[3]}. {opposing_pkmn.get_name()} avoided the attack.")
                    continue

                # print("Is crit", is_crit)
                if is_crit:
                    crit_damage = 1.5
                    crit_statement = " It's a critical hit!"
                
                effectiveness, STAB = self.effectiveness_calculations(battles, moves_dict, type_matchup, opposing_pkmn)

                if moves_dict[battles[3]]['damage_class'].lower() == "physical":
                    outcome = self.physical_special_splits(
                        "physical", battles[1], opposing_pkmn, STAB, moves_dict, battles, \
                        effectiveness, crit_damage, damage_divider, self.get_trainer_1(), self.TRAINER_1_ACTIVE, crit_statement)
                    if outcome == "Done":
                        return

                elif moves_dict[battles[3]]['damage_class'].lower() == "special":
                    outcome = self.physical_special_splits(
                        "special", battles[1], opposing_pkmn, STAB, moves_dict, battles, \
                        effectiveness, crit_damage, damage_divider, self.get_trainer_1(), self.TRAINER_1_ACTIVE, crit_statement)
                    if outcome == "Done":
                        return
    
    def effectiveness_calculations(self, battle_move, moves_dict, type_matchup, opposing_pkmn):
         # Super effective, neutral or not very effective
        effectiveness = 1
        STAB = 1
        for opposing_type in opposing_pkmn.get_types():
            effectiveness *= type_matchup[opposing_type][moves_dict[battle_move[3]]['type']]

        if moves_dict[battle_move[3]]['type'] in battle_move[1].get_types():
            STAB = 1.5
        
        return effectiveness, STAB

    def physical_special_splits(self, move_type, attack_pkmn, defense_pkmn, STAB, moves_dict, battle_move, \
                                effectiveness, crit_damage, damage_divider, trainer_2, trainer_2_active, crit_statement):
        atk = 0
        defense = 0
        
        if move_type == "physical":
            atk = attack_pkmn.get_atk()
            defense = defense_pkmn.get_def()
        
        elif move_type == "special":
            atk = attack_pkmn.get_sp_atk()
            defense = defense_pkmn.get_sp_def()

        total_dmg = math.floor(
            (atk / defense) * moves_dict[battle_move[3]]['power'] * STAB * effectiveness * crit_damage / damage_divider)
        
        print("Total damage", total_dmg)
        defense_pkmn.reduce_hp(total_dmg)
        print(f"{battle_move[1].get_name()} used {battle_move[3]}{self.print_effectiveness(effectiveness)}.{crit_statement}")
        print(f"{defense_pkmn.get_name()} is now on {defense_pkmn.get_hp()}HP")
        if defense_pkmn.get_hp() <= 0:
            print(f"{defense_pkmn.get_name()} has fainted.")
            # Need to switch in Pokemon from the back
            switch_moves = self.switch_selection(trainer_2, trainer_2_active)
            in_the_back = self.process_switch(switch_moves)
            if not in_the_back:
                return "Done"

    def print_effectiveness(self, effectiveness):
        if effectiveness <= 0.5:
            return " It's not very effective."
        
        elif effectiveness >= 2:
            return " It's super effective!"
        
        else:
            return ""

if __name__ == "__main__":
    pass