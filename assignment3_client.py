from _thread import *
import threading
from datetime import datetime
import logging
import time
import socket
import requests
import json
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipAddress = "localhost"
port = 12345

players = '0'

def main():
    #matchCount = input("How many games should the simulation play? ")
    sock.connect((ipAddress, port))
    sock.sendto(bytes(players,'utf8'), (ipAddress, port))


if __name__ == '__main__':
   main()