#! /bin/python3
import subprocess
import json
from os import path
from time import sleep

with open('./all_fifa_players.json') as fp:
    listObj = json.load(fp)
    players = listObj['players']

    for page in range(1, 931):
        print(page)
        
        # Utilizing FutDB's Ultimate Team API to get player data,        
        """
        curl -s -X 'GET' \
        'https://futdb.app/api/players?page=1100000' \                                                                                -H 'accept: application/json' \
        -H 'X-AUTH-TOKEN: {token}'
        """

        arguments = ["curl", "-s", "-X", "GET", f"https://futdb.app/api/players?page={page}", 
                    "-H", "accept: application/json", "-H", "X-AUTH-TOKEN: {token}"]
        result = subprocess.run(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        output = json.loads(result.stdout)

        for i in output["items"]:
            
            player_dict = {
                "id": i["id"],
                "name": i["name"],
                "birthDate": i["birthDate"], 
                "age": i["age"], 
                "league": i["league"], 
                "nation": i["nation"],
                "position": i["position"], 
                "color": i["color"], 
                "rating": i["rating"], 
                "rarity": i["rarity"], 
                "resourceBaseId": i["resourceBaseId"],
                "club": i["club"]
            }
            
            players[player_dict["id"]] = player_dict

with open('./all_fifa_players.json', 'w') as fp:
    json.dump({'players': players}, fp, indent=4)