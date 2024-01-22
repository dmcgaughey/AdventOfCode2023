import numpy as np

def calc_hash(instr):
  hash = 0
  for c in instr:
    if c in [',','\n']: break
    hash = ((hash + ord(c)) * 17) % 256
  return hash

def insert_to_box(boxes, item):
  # Check for empty list
  if not boxes:
    boxes.append(item)
    return

  label = item[0]
  for cnt in range(len(boxes)):
    # look for matching label
    if boxes[cnt][0] == label:
      boxes[cnt][1] = item[1]
      break
  else:
      boxes.append(item)
  return

def remove_from_box(boxes,item):
  if not boxes:
    return
  for cnt in range(len(boxes)):
    if boxes[cnt][0]==item[0]:
      # Found position to delete
      boxes.pop(cnt)
      break
  return

def calc_power(box):
  print(box)
  if not box:
    return 0
  power = 0
  for cnt in range(len(box)):
    power += (cnt+1)*box[cnt][1]
  return power

## Part 2     Find the weight of rock on a table
# with open('Dec15test.txt','r') as f:
with open('Dec15.txt','r') as f:
  lines = f.readlines()

line = lines[0]
eol = line.count('\n')
line = line.replace('\n',',')
Groups = line.split(',')

boxesList =  [ [] for _ in range(256) ]

for group in Groups:
  if group.count('=')>0:
    item = group.split('=')
    item[1] = int(item[1])
    insert_to_box(boxesList[calc_hash(item[0])], item)
  elif group.count('-')>0:
    item = group.split('-')
    remove_from_box(boxesList[calc_hash(item[0])],item)

powerList = []
for cnt in range(256):
  powerList.append(calc_power(boxesList[cnt]))

totalPower = np.sum(np.array(powerList) * (np.arange(1,257)) )

print(totalPower)


## Main for Part 2