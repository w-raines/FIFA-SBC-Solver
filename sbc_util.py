import math

# Calculate ratings based on Rating formula, found here:
# https://www.fifaah.com/news/1290--fifa-19-sbc-squad-ratings-formula--combinations---how-to-build-the-cheapest-87-86-85-84-rated-teams.html
def calculate_ratings(ratings):
    base_sum = 0
    for rating in ratings:
        base_sum += int(rating)

    base_avg = base_sum / 11
    add_sum = 0
    
    for rating in ratings:
        if (int(rating) > math.floor(base_avg)):
            add_sum += int(rating) - math.floor(base_avg)

    final_rating = math.floor(base_avg + (add_sum / 11))
    
    return int(final_rating)

# Calculate chemistry based on the chemistry formula, found here:
# https://www.rockpapershotgun.com/fifa-23-chemistry#:~:text=Chemistry%20will%20only%20add%20to,max%20chemistry%20with%20a%20player
def calculate_chemistry(selected_ids, player_data):
    club_counts = {}
    league_counts = {}
    nation_counts = {}
    player_chem = {}

    for id in selected_ids:
        club = player_data[id]['club']
        league = player_data[id]['league']
        nation = player_data[id]['nation']

        if club not in club_counts:
            club_counts[club] = 0
        if league not in league_counts:
            league_counts[league] = 0
        if nation not in nation_counts:
            nation_counts[nation] = 0

        player_chem[id] = 0
        club_counts[club] += 1
        league_counts[league] += 1
        nation_counts[nation] += 1

    for id in selected_ids:
        total_chemistry = 0
        
        club = player_data[id]["club"] 
        league = player_data[id]["league"]
        nation = player_data[id]["nation"]
        
        if club_counts[club] >= 7:
            total_chemistry += 3
        elif club_counts[club] >= 4:
            total_chemistry += 2
        elif club_counts[club] >= 2:
            total_chemistry += 1

        if league_counts[league] >= 8:
            total_chemistry += 3
        elif league_counts[league] >= 5:
            total_chemistry += 2
        elif league_counts[league] >= 3:
            total_chemistry += 1

        if nation_counts[nation] >= 8:
            total_chemistry += 3
        elif nation_counts[nation] >= 5:
            total_chemistry += 2
        elif nation_counts[nation] >= 2:
            total_chemistry += 1
            
        player_chem[id] = total_chemistry


    output_chemistry = 0
    
    for id in selected_ids:
        if player_chem[id] >= 3:
            output_chemistry += 3
        else:
            output_chemistry += player_chem[id]
    
    return int(output_chemistry), player_chem

# Check if a squad has a minimum number of unique countries/nationalities
def check_min_countries(selected_ids, player_data, num_uniq_countries):
    unique_countries = set()

    for id in selected_ids:
        unique_countries.add(player_data[id]['nation'])

    return len(unique_countries) >= num_uniq_countries

# Check if a squad has a minimum number of unique leagues
def check_min_leagues(selected_ids, player_data, num_uniq_leagues):
    unique_leagues = set()

    for id in selected_ids:
        unique_leagues.add(player_data[id]['league'])

    return len(unique_leagues) >= num_uniq_leagues

# Check if a squad has a minimum number of unique clubs
def check_min_clubs(selected_ids, player_data, num_uniq_clubs):
    unique_clubs = set()

    for id in selected_ids:
        unique_clubs.add(player_data[id]['club'])

    return len(unique_clubs) >= num_uniq_clubs

# Prints out the solution along with data about the requirement
def print_output(player_chem, player_data, rating_req, chemistry_req, min_club, min_league, min_nation):
    player_ids = list(player_chem.keys())
    ratings = [player_data[player_id]['rating'] for player_id in player_ids]
    positions = [player_data[player_id]['position'] for player_id in player_ids]
    chemistries = list(player_chem.values())
    positions_filled = [player_data[player_id]['position'] for player_id in player_ids]
    player_names = [player_data[player_id]['name'] for player_id in player_ids]

    squad_chemistry = calculate_chemistry(player_ids, player_data)
    num_clubs = len(set([player_data[player_id]['club'] for player_id in player_ids]))
    num_leagues = len(set([player_data[player_id]['league'] for player_id in player_ids]))
    num_nations = len(set([player_data[player_id]['nation'] for player_id in player_ids]))

    print("Required\tActual")
    
    print("Rating:", rating_req, '\t', calculate_ratings(ratings))
    print("Chemistry:", chemistry_req, '\t', squad_chemistry[0])
    print("Clubs:", min_club, '\t', num_clubs)
    print("Leagues:", min_league, '\t', num_leagues)
    print("Nations:", min_nation, '\t', num_nations, '\n')

    print("Players:", player_ids)
    for i in range(len(player_ids)):
        player_id = player_ids[i]
        player_name = player_names[i]
        rating = ratings[i]
        position = positions[i]
        chemistry = chemistries[i]
        print(player_id, player_name, rating, position, chemistry)

       

