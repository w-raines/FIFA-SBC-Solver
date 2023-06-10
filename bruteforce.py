import json
import random
import time
from sbc_util import *

class BruteForceSolver():
    
    def __init__(self, players="all_fifa_players.json", requirements="sbc_requirements.json", formations="formations.json"):
        
        with open(requirements, 'r') as file:
            self.sbc_data = json.load(file)
        with open(players, 'r') as file:
            self.player_data = json.load(file) 
        with open(formations, 'r') as file:
            self.formation_data = json.load(file)

        # Get the json data for players, sbcs, and formation
        self.player_ids = list(self.player_data.keys())
        self.sbc_ids = list(self.sbc_data.keys())
        self.formation_ids = list(self.formation_data.keys())
    
    # Attempts to solve the sbc of requirement_id, runs until a solution is found    
    def solve_sbc(self, requirement_id):
        chem, rating, iterations = 0, 0, 0
        
        formation_req = self.sbc_data[requirement_id]["formation"]
        rating_req = int(self.sbc_data[requirement_id]["rating"])
        chemistry_req = int(self.sbc_data[requirement_id]["min_total_chemistry"])
        min_club_req = int(self.sbc_data[requirement_id]["min_club"])
        min_nation_req = int(self.sbc_data[requirement_id]["min_nationality"])
        min_league_req = int(self.sbc_data[requirement_id]["min_league"])

        while True:
            iterations += 1
            team = {}
            selected_player_ids = []
            selected_player_base_ids = [] # Use to prevent duplicate players if they have multiple cards
            selected_player_rating = []

            random.shuffle(self.player_ids) # Shuffle players so we don't get the same result every time
            
            for position, count in self.formation_data[formation_req].items():
                team[position] = []

                # Looping through players
                for player in self.player_ids:
                    
                    # If player's position matches and not already selected
                    if self.player_data[player]['position'] == position and self.player_data[player]['id'] not in selected_player_ids and self.player_data[player]['resourceBaseId'] not in selected_player_base_ids:
                        team[position].append(player)
                        selected_player_ids.append(player)
                        selected_player_base_ids.append(self.player_data[player]['resourceBaseId'])
                        selected_player_rating.append(self.player_data[player]['rating'])

                        # If we found enough players for this position
                        if len(team[position]) == count:
                            break

            chem, player_chem = calculate_chemistry(selected_player_ids, self.player_data)
            rating = calculate_ratings(selected_player_rating)
            
            # Check if players meet requirements
            if (chem >= chemistry_req and 
                rating >= rating_req and 
                check_min_clubs(selected_player_ids, self.player_data, min_club_req) and 
                check_min_countries(selected_player_ids, self.player_data, min_nation_req) and 
                check_min_leagues(selected_player_ids, self.player_data, min_league_req)
                ):
                
                print_output(player_chem, self.player_data, rating_req, chemistry_req, min_club_req, min_league_req, min_nation_req)
                print("Iterations: ", iterations)
                return
  
mysolve = BruteForceSolver()

start_time = time.time()
mysolve.solve_sbc("343492")
end_time = time.time()

print("time: ", end_time - start_time)