
from _thread import *
import threading
from datetime import datetime
import logging
import time
import socket
import requests
import json

URL = "https://vfrlx7pdxl.execute-api.us-east-1.amazonaws.com/default/hello-world"
API_KEY = "tFm7YmutpZ9nZ9NuWi0Hda96PgxdcvJw3ktOx6bz"  # API key
headers = { "x-api-key": API_KEY }

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345

def main():
    sock.bind(('', port))
    start_new_thread(MakeApiRequestToGetPlayers, (sock,))
    while True:
        time.sleep(1)
        start_new_thread(ActiveIndicator, (sock,))


def MakeApiRequestToGetPlayers(sock):
    while True:
        sock.listen()
        data, addr = sock.accept()

        response = requests.get(URL, headers=headers)
        body = json.loads(response.content)
        players = body.get('Items')

        #Debugging
        for player in players:
            print("Player ID: " + player['player_id'])
            print("Player Name: " + player['player_name'])
            print("Player Skill: " + player['player_skill'])
            print("------------------")

def ActiveIndicator(sock):
    print("Server listening...")

def MakeMatch():
    print("hi")

if __name__ == '__main__':
   main()