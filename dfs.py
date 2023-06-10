import json
import random
import math
from sbc_util import *
import time

class DFSSolver():
    
    def __init__(self, players="all_fifa_players.json", requirements="sbc_requirements.json", formations="formations.json", min_club=1, min_league=1, min_nation=1):
        
        # Load data from JSON files
        with open(requirements, 'r') as file:
            self.sbc_data = json.load(file)
        with open(players, 'r') as file:
            self.player_data = json.load(file) 
        with open(formations, 'r') as file:
            self.formation_data = json.load(file)

        self.player_ids = list(self.player_data.keys())
        random.shuffle(self.player_ids)  # Shuffle the players
        self.sbc_ids = list(self.sbc_data.keys())
        self.formation_ids = list(self.formation_data.keys())

        self.min_club = min_club
        self.min_league = min_league
        self.min_nation = min_nation

    def prune(self, team, formation_req, rating_req, chemistry_req):
        # Calculate the maximum remaining chemistry and rating
        max_remaining_chem = 3 * (11 - len(team))
        max_remaining_rating = 99 * (11 - len(team))

        # Calculate the current chemistry and rating
        current_chem, player_chem = calculate_chemistry(team, self.player_data)
        current_ratings = [self.player_data[player]['rating'] for player in team]
        current_rating = calculate_ratings(current_ratings)

        # If even the maximum possible chemistry and rating can't meet the requirements, prune this branch
        if current_chem + max_remaining_chem < chemistry_req or current_rating + max_remaining_rating < rating_req:
            return True

        # Check if the minimum club, league, and nation requirements are met
        if len(team) >= 6:
            if not check_min_clubs(team[:6], self.player_data, self.min_club):
                return True
            if not check_min_leagues(team[:6], self.player_data, self.min_league):
                return True
            if not check_min_countries(team[:6], self.player_data, self.min_nation):
                return True

        return False

    def dfs(self, node, formation_req, positions_filled, rating_req, chemistry_req):
        # Prune the branch if the requirements cannot be met
        if self.prune(node, formation_req, rating_req, chemistry_req):
            return None

        # Return the current team if it is complete and meets the requirements
        if len(node) == 11:
            chem, player_chem = calculate_chemistry(node, self.player_data)
            current_ratings = [self.player_data[player]['rating'] for player in node]
            rating = calculate_ratings(current_ratings)
            if chem >= chemistry_req and rating >= rating_req:
                return node
            else:
                return None

        positions = list(self.formation_data[formation_req].keys())

        for player in self.player_ids:
            player_pos = self.player_data[player]['position']
            if player not in node and player_pos in positions and positions_filled[player_pos] < self.formation_data[formation_req][player_pos]:
                positions_filled[player_pos] += 1
                solution = self.dfs(node + [player], formation_req, positions_filled, rating_req, chemistry_req)
                if solution is not None:
                    return solution
                positions_filled[player_pos] -= 1

        return None

    def solve_sbc(self, requirement_id):
        formation_req = self.sbc_data[requirement_id]["formation"]
        rating_req = int(self.sbc_data[requirement_id]["rating"])
        chemistry_req = int(self.sbc_data[requirement_id]["min_total_chemistry"])

        positions_filled = {pos: 0 for pos in self.formation_data[formation_req].keys()}

        # Run the DFS algorithm to find a solution
        team = self.dfs([], formation_req, positions_filled, rating_req, chemistry_req)
        if team is not None:
            chem, player_chem = calculate_chemistry(team, self.player_data)
            print_output(player_chem, self.player_data, rating_req, chemistry_req, self.min_club, self.min_league, self.min_nation)


start_time = time.time()
mysolve = DFSSolver(min_club=6, min_league=3, min_nation=4)
mysolve.solve_sbc("343492")
end_time = time.time()

print("time:", end_time - start_time)
