from py_files.pokemon import Pokemon

class Trainer:
    def __init__(self, name):
        self.name = name
        self.team = list()
    
    def get_name(self):
        return self.name

    def get_team(self):
        return self.team

    def print_team(self):
        for i, pkmn in enumerate(self.team):
            print(f"{i + 1} - {pkmn.get_name()}")
    
    # def trainer_options(self):
    #     print("1 - Battle\n2- Pokemon")
    
    def add_pokemon(self, mon: Pokemon):
        if len(self.team) < 6:
            self.team.append(mon)
            print(f"{mon.name} added successfully")
            return mon
        
        print(f"Unable to add {mon.name}. Already have 6 in the party")
    
    def remove_pokemon(self, mon: Pokemon):
        if mon.name not in self.team:
            print(f"{mon.name} is not in party")
            return
        
        self.team.remove(mon)
        print(f"New party: {self.team}")
        return self.team # New team