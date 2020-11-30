
from _thread import *
import threading
from datetime import datetime
import logging
import logging.config
import time
import socket
import requests
import json

URL = "https://vfrlx7pdxl.execute-api.us-east-1.amazonaws.com/default/hello-world"
API_KEY = "tFm7YmutpZ9nZ9NuWi0Hda96PgxdcvJw3ktOx6bz"  # API key
headers = { "x-api-key": API_KEY }

skillThreshold = 650

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345

def main():
    logging.basicConfig(filename='Assignment3Server.log', level=logging.INFO)
    sock.bind(('', port))
    start_new_thread(MakeApiRequestToGetPlayers, (sock,))
    while True:
        time.sleep(1)
        start_new_thread(ActiveIndicator, (sock,))


def MakeApiRequestToGetPlayers(sock):
    while True:
        #Listen for a connection from a client.
        sock.listen()

        #Data recieved and from where stored in variables.
        data, addr = sock.accept()

        #The data (ID of player in this case) stored as a string.
        RequesterID = data.recv(1024)
        RequesterID = RequesterID.decode("utf-8")
        print("Player ID #" + RequesterID + " looking for a match.")
        logging.info('The player ID#' + RequesterID + ' has connected.')

        #Get all the items from the player_id database
        response = requests.get(URL, headers=headers)
        body = json.loads(response.content)
        players = body.get('Items')

        response = MakeMatch(players, RequesterID)
        data.send(bytes(response, 'utf8'))
        

def ActiveIndicator(sock):
    print("Server listening...")

def MakeMatch(players, RequesterID):
    #Get the player information of the player requesting the match
    for player in players:
        if player['player_id'] == RequesterID:
            RequestingPlayer = player

    #Attempt to find players suitable to play with this player.

    playersByAscendingSkillLevel = sorted(players, key=lambda elem: elem['player_skill'])

    matchMakedPlayers = []
    matchMakedPlayers.append(RequestingPlayer)

    for player in players:
        if player != RequestingPlayer and abs(player['player_skill'] - RequestingPlayer['player_skill']) < skillThreshold:
            if len(matchMakedPlayers) < 3:
                matchMakedPlayers.append(player)

    #for player in matchMakedPlayers:
    #    print("Player ID: " + player['player_id'])
    #    print("Player Name: " + str(player['player_name']))
    #    print("Player Skill: " + str(player['player_skill']))
    #    print("------------------")

    response = json.dumps(matchMakedPlayers)
    return response

if __name__ == '__main__':
   main()