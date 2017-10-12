#!/usr/bin/python3

import socket
import random
import json
import sys

MY_SHOTS = [[None for r in range(10)] for c in range(10)]
OPPONENT_SHOTS = []
LAST_SHOT = None
      
def get_name():
  """Returns the name of the client"""
  return "Boss"

def get_ship_placements():
  """Returns the locations and orientations of the ships"""
  return json.dumps({"B":[random.randint(0,5),random.randint(0,1),"h"],
                     "S":[random.randint(0,5),random.randint(2,3),"h"],
                     "D":[random.randint(0,5),random.randint(4,5),"h"],
                     "P":[random.randint(0,5),random.randint(6,7),"h"],
                     "C":[random.randint(0,5),random.randint(8,9),"h"]})

def get_shot_location():
  """Returns the point to shoot at"""
  global LAST_SHOT
  available = [(x, y) for x in range(10) for y in range(10) if MY_SHOTS[x][y] is None]
  coords = random.choice(available)
  LAST_SHOT = coords
  return json.dumps(coords)

def process_input(data):
  """Processes the input from the server
  
  Return a string to send a response
  Return False to exit the client
  Return None to continue normally
  """
  if data == "NAME":
    return get_name()
    
  elif data == "SHIP PLACEMENT":
    return get_ship_placements()
  
  elif data == "SHOT LOCATION":
    return get_shot_location()
  
  elif data == "MISS":
    MY_SHOTS[LAST_SHOT[0]][LAST_SHOT[1]] = data
  
  elif data == "HIT":
    MY_SHOTS[LAST_SHOT[0]][LAST_SHOT[1]] = data
  
  elif data[:4] == "SUNK":
    MY_SHOTS[LAST_SHOT[0]][LAST_SHOT[1]] = data
  
  elif data[:13] == "OPPONENT SHOT":
    tokens = data[14:].split(",")
    OPPONENT_SHOTS.append((int(tokens[0]), int(tokens[1]), tokens[2]))
  
  elif data == "WIN":
    return False
  
  elif data == "LOSE":
    return False
  
  elif data == "ERROR":
    return False
    
  return None

def main(args):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
  host = args["h"]
  port = args["p"]
  
  sock.connect((host, port))
  
  while True:
    data = sock.recv(4096).decode("utf-8").strip()
    for command in data.split("\r\n"):
      print(command)
      response = process_input(command)
      if response is False:
        break
      if response:
        sock.sendall(response.encode("utf-8"))
      
  sock.close()
      

def get_args():
  args = {"h": "localhost", "p": 4949}
  for i in range(len(sys.argv)):
    if sys.argv[i][0] == "-":
      arg = sys.argv[i+1] if i+1 < len(sys.argv) else ""
      try:
        arg = int(arg)
      except:
        pass
      args[sys.argv[i][1]] = arg
  return args

if __name__ == "__main__":
  args = get_args()
  main(args)
