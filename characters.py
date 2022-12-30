import json
import requests
import time
from bs4 import BeautifulSoup

while True:
  url = 'https://www.tibia.com/community/?subtopic=worlds'
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  world_links = soup.find_all('a')
  online_players = []

  for link in world_links:

    if 'subtopic=worlds&world=' in link.get('href', ''):
      response = requests.get(link['href'])
      soup = BeautifulSoup(response.text, 'html.parser')
      player_elements = soup.find_all('a', {'href': lambda x: x and x.startswith('https://www.tibia.com/community/?subtopic=characters&name=')})
      players = [player.text.replace('\xa0', ' ') for player in player_elements]
      online_players.extend(players)

  sorted_online_players = sorted(online_players)

  try:
    with open('online_players.json', 'r') as f:
      previous_players = json.load(f)
  except:
    previous_players = []

  new_players = [player for player in sorted_online_players if player not in previous_players]
  print(f'Added {len(new_players)} new players to JSON file.')
  previous_players.extend(new_players)

  with open('online_players.json', 'w') as f:
    json.dump(previous_players, f, indent=2)

  print(f'Total of {len(previous_players)} players in JSON file.\n')

  time.sleep(600)