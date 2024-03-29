# -*- coding: utf-8 -*-
"""Dec4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UMV7Eydx2Dd6qGDyvL9bE5C6GT2GWceb
"""

import numpy as np

with open('Dec4.txt','r') as f:
  lines = f.readlines()

line_in = lines[0]
split1=line_in.split(':')
#split1[0].split()
gameid = int(split1[0].split()[1])
gamesplit = split1[1].split('|')
winning = gamesplit[0].split()
drawn = gamesplit[1].split()
winning = set([int(x) for x in winning])
drawn = set([int(x) for x in drawn])
#temp = winning.intersection(drawn)
num = len(winning.intersection(drawn))
points = (2**(num-1)) if num>0 else 0

# Create a function to process a line and create a dictionary of each trial
def process_line(line_in):
  # Split the game number from the games
  split1 = line_in.split(':')
  gameid = int(split1[0].split()[1])

  # Now split the winning numbers from the drawn numbers using | seperator
  gamesplit = split1[1].split('|')
  winning = gamesplit[0].split()
  drawn = gamesplit[1].split()

  # Convert to sets of integers
  winning = set([int(x) for x in winning])
  drawn = set([int(x) for x in drawn])
  # Find number of common numbers in each set
  num = len(winning.intersection(drawn))

  # Calculate the number of points for this line
  points = (2**(num-1)) if num>0 else 0
  #print([gameid, num, points])
  return [gameid, num, points]

# Create the main loop to process all the lines, identify the invalid games and
# sum the ids of the invalid game
points = 0
num_lines = len(lines)

ids =np.zeros(num_lines, dtype=int)
num_matches = np.zeros(num_lines, dtype=int)
num_cards = np.ones(num_lines, dtype=int)
game_points = np.zeros(num_lines, dtype=int)

for cnt in range(num_lines):
  [ids[cnt], num_matches[cnt], game_points[cnt]] = process_line(lines[cnt])
  points += game_points[cnt]

# Points for part 1
print(f'Part1: Total Points: {points}')

# For Part 2 process the array and add on the number of additional cards
for card_id in range(num_lines):
  for new_cards in range(num_matches[card_id]):
    if (card_id+new_cards+1)<num_lines:
      num_cards[card_id+new_cards+1] += num_cards[card_id]

print(f'Part2: Number cards: {sum(num_cards)}')

num_cards

num_matches

