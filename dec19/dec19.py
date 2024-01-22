import numpy as np
import itertools
import types
from enum import IntEnum

PROCESSItem = dict['expression':str, 'dest':str]
Process = dict['name':str, 'plist':list[PROCESSItem]]
ProcessList = list[Process]

def parse_process(ProcessList,instr)->Process:
  name, split1 = instr.strip().strip('}').split('{')
  split2 = split1.split(',')
  PItemList: list[PROCESSItem] = []
  for p in split2:
    if p=='A' or p=='R':
      expression = p
      dest = ''
    else:
      if '>' in p or '<' in p:
        expression, dest = p.split(':')
      else:
        expression = 'True'
        dest = p
    PItemList.append({'expression':expression, 'dest':dest})

  return Process({'name':name, 'plist': PItemList})


# x,m,s,a = 0,0,0,0
def run_process(ProcessList, process_str):
  global x,m,s,a
  # Split up the process lines and initialize the process variable
  for cmd in process_str.split(','):
    # _locals = locals()
    exec(cmd) #,globals,{'x':x,'s':s,'a':a,'m':m}) #,globals(),_locals)

  next_cmd = 'in'
  # Find process
  while next_cmd:
    # Find process of given name
    if next_cmd =='A' or next_cmd =='R':
      accepted = next_cmd =='A'
      break
    for process in ProcessList:
      if process['name'] == next_cmd: break

    # Run list of processes
    for p in process['plist']:
        if p['expression'] == 'A':  # accept
          next_cmd=''
          accepted = True
          break
        elif p['expression'] == 'R':
          next_cmd=''
          accepted = False
          break
        elif eval(p['expression']):
          next_cmd = p['dest']
          break
    else:
      accepted = False
      next_cmd=''
      break
  out = eval('x+m+s+a')
  return (accepted,process_str, out)


# PROCESSItem:dict['expression':str, 'dest':str]
# Process: dict['name':str, list[PROCESSItem]] = []
ProcessList:list[Process] = []

## Part 1     Process the parts and
# with open('dec19Test.txt','r') as f:
with open('dec19.txt','r') as f:
  lines = f.readlines()

for line in enumerate(lines,0):
  if line[1] != '\n':
    ProcessList.append(parse_process(ProcessList,line[1]))
  else:
    break

total_cost = 0
for line in lines[line[0]+1:]:
  valid, process_str, cost = run_process(ProcessList,line[1:-2])
  if valid: total_cost += cost

print(f'Total Cost: {total_cost}')


#############
# Part 2
#############

class Part(IntEnum):
  a = 0
  m = 1
  s = 2
  x = 3

# Analyze the processes for valid ranges of a, x, s and m that are valid
SUBSET = dict['part':Part,'start':int, 'end':int]
RangeList = list[SUBSET, SUBSET, SUBSET, SUBSET]
ValidList = tuple[str, RangeList]

class Operator(IntEnum):
  gt = 0
  lt= 1

def calcCombs(rangeL:RangeList)->int:
  combs = 1
  for cnt in range(4):
    combs *= (rangeL[cnt]['end']-rangeL[cnt]['start']+1)
  return combs

def analyzeRanges(InitProcess:str,PList:ProcessList)->ValidList:
  initSubset = [{'part':Part['a'],'start':1,'end':4000}, {'part':Part['m'],'start':1,'end':4000},
               {'part':Part['s'],'start':1,'end':4000}, {'part':Part['x'],'start':1,'end':4000}]

  queue = [ ('in', tuple(initSubset))]
  total_combs = 0
  while queue:
    cmd, subset = queue.pop()
    subset = list(subset)

    # Find process of given name
    if cmd == 'R':
      continue

    if cmd == 'A':
        total_combs += calcCombs(subset)
        continue

    # Find the process for cmd in the list
    for process in PList:
      if process['name'] == cmd:  break

    # Apply ranges as appropriate for each process in PList
    for p in process['plist']:
        if p['expression'] == 'A':  # accept
          total_combs += calcCombs(subset)
          break
        elif p['expression'] == 'R':
          break
        else:
          # Parse expression and determine ranges
          if not ('>' in p['expression'] or '<' in p['expression']):
            queue.append((p['dest'], tuple(subset)))
            break
          else:
            var = Part[p['expression'][0]]
            op = Operator.gt if p['expression'][1]=='>' else Operator.lt
            val = int(p['expression'][2:])

          # Now adjust the subset depending upon operator
          r = subset[var]
          match op:
            case Operator.gt:
              if r['end']<=val: continue

              # Add new subset and new process to Q
              tempRange = [x.copy() for x in subset]
              tempRange[var]['start'] = val+1       # = subset({'name':p['dest'], 'start':val, 'end':p['end']})
              queue.append( (p['dest'], tuple(tempRange)))

              # Update subset for next process
              subset[var]['end'] = val          #SUBSET({'name': p['dest'], 'start': p['start'], 'end': val - 1})
              #continue

            case Operator.lt:
              if r['start'] >= val: continue

              # Add new subset and new process to Q
              tempRange = [x.copy() for x in subset]
              tempRange[var]['end'] = val-1
              queue.append( (p['dest'], tuple(tempRange)) )

              # Update subset for next process
              subset[var]['start'] = val  # SUBSET({'name': p['dest'], 'start': p['start'], 'end': val - 1})

  return total_combs


cost = analyzeRanges('in',ProcessList)
print(cost)


## Main for Part 2