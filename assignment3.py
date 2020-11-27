
import logging
import requests
import json

def MakeApiRequest():
    URL = "https://vfrlx7pdxl.execute-api.us-east-1.amazonaws.com/default/hello-world"
    API_KEY = "tFm7YmutpZ9nZ9NuWi0Hda96PgxdcvJw3ktOx6bz" #API key

    headers = {
        "x-api-key": API_KEY
    }

    response = requests.get(URL, headers=headers)
    body = json.loads(response.content)
    players = body.get('Items')

    for player in players:
        print("Player ID: " + player['player_id'])
        print("Player Name: " + player['player_name'])
        print("Player Skill: " + player['player_skill'])
        print("\n")
    
   # print(result)

def main():
    MakeApiRequest()

main()