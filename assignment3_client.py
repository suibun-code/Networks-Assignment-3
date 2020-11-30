from _thread import *
import threading
from datetime import datetime
import logging
import time
import socket
import requests
import json
import random

UpdateSkillURL = "https://94ghzerne7.execute-api.us-east-1.amazonaws.com/default/UpdateElo"
UpdateAPI_KEY = "1trpw9xEYPPt38nOp2LrawmtEgjhiPK3lOKVaALi"
Updateheaders = { "x-api-key": UpdateAPI_KEY}

GetPlayersURL = "https://vfrlx7pdxl.execute-api.us-east-1.amazonaws.com/default/hello-world"
PlayersAPI_KEY = "tFm7YmutpZ9nZ9NuWi0Hda96PgxdcvJw3ktOx6bz"
Playersheaders = { "x-api-key": PlayersAPI_KEY}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipAddress = "localhost"
port = 12345

#To actually simulate the matches, a preset of player IDs need to be
#stored so we can test this. Otherwise 3 clients would need to be opened.
#All other IDs other than the one sent to the server are considered already 'matchmaking'.
players = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def main():
    logging.basicConfig(filename='Assignment3.log', level=logging.INFO)

    i = 0
    matchCount = input("How many games should the simulation play? ")
    logging.info('Simulating ' +  matchCount + ' matches.')

    while i < int(matchCount):
        logging.info('Beginning Game#' + str(i))
        thisPlayer = random.choice(players)
        SimulateMatchmaking(thisPlayer)
        i += 1

def SimulateMatchmaking(thisPlayer):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ipAddress, port))
        sock.sendto(bytes(thisPlayer, 'utf8'), (ipAddress, port))
        data = sock.recv(1024)

    matchMakedPlayers = json.loads(data)
    logging.info('Matched players: ' + matchMakedPlayers[0]['player_name'] + ', ' + matchMakedPlayers[1]['player_name'] + ', ' + matchMakedPlayers[2]['player_name'])

    winningPlayer = random.choice(matchMakedPlayers)
    matchMakedPlayers.remove(winningPlayer)

    print("Player that won: " + winningPlayer['player_name'])
    logging.info('Winning player: ' + winningPlayer['player_name'])
    logging.info('player skill: ' + str(winningPlayer['player_skill']))

    #Update the winning player's skill
    params = {'player_id': winningPlayer['player_id'], 'result': 1}
    requests.get(UpdateSkillURL, headers=Updateheaders, params=params)

    #Update the lossing player's skills
    print("Players that lost:")
    print("------------------")
    for player in matchMakedPlayers:
        print("Player Name: " + str(player['player_name']))
        params = {'player_id': player['player_id'], 'result': 0}
        requests.get(UpdateSkillURL, headers=Updateheaders, params=params)
        logging.info('Losing player: ' + player['player_name'])
        logging.info('player skill: ' + str(player['player_skill']))

if __name__ == '__main__':
   main()
