from enum import IntEnum
from queue import Queue

class CTYPE(IntEnum):
	NONE = -1
	BROADCASTER = 0
	FLIPFLOP = 1
	CONJUNCTION = 2

nameList = []
def get_name_indx(name):
	global nameList
	if name not in nameList:
		name_indx = len(nameList)
		nameList.append(name)
	else:
		name_indx = nameList.index(name)
	return name_indx


def is_zero_state(process_nodes):
	# Check for all flip_flops to be 0 for stopping condition
	for node in process_nodes:
		if node['type'] == CTYPE.FLIPFLOP or node['type'] == CTYPE.CONJUNCTION:
			if any(node['state']):
				return False
	return True  # all FLIP_FLOPS and CONJUNCTION are back at 0 state


target_found = False
def run_process(process_nodes,target_process=-1)->tuple:
	global target_found

	processQ = Queue(maxsize=100)
	processQ.put((0,0,0))		#process, source, signal
	num_pulses = [1,0]
	# print(f'From: {-1} to {0} Signal {0}')

	while not processQ.empty():
		process, source, signal = processQ.get()

		match process_nodes[process]['type']:
			case CTYPE.FLIPFLOP:
				SEND = not signal
				if signal==0:
					process_nodes[process]['state'][0] = int(not process_nodes[process]['state'][0])
					next_signal = process_nodes[process]['state'][0]
			case CTYPE.CONJUNCTION:
				SEND = True
				indx = process_nodes[process]['sources'].index(source)	# Process the signal came from
				process_nodes[process]['state'][indx] = signal
				next_signal = int ( not all(process_nodes[process]['state']) )
			case CTYPE.BROADCASTER:		# Should alway be 0
				SEND = True
				next_signal = signal
			case CTYPE.NONE:
				continue

		if SEND:		# FLIP_FLOPS only send when low received
			for dest in process_nodes[process]['dests']:
				num_pulses[next_signal] += 1
				processQ.put((dest, process, next_signal))
				# print(f'From: {process} to {dest} Signal {next_signal}')

		if process == target_process:
			if next_signal == 1:
				target_found = True

		# if STOP:
		# 	continue
		# if process_nodes[process]['type'] != CTYPE.BROADCASTER and is_zero_state(process_nodes):
		# 	break

	return tuple(num_pulses)

########################
# Part 1: Process button process through a machine of flip-flops and conjunction modules
########################
# with open('dec20test.txt', 'r') as f:
# with open('dec20testB.txt', 'r') as f:
with open('dec20.txt', 'r') as f:
	lines = f.readlines()
f.close()

lines.sort(key=lambda x: x.split()[0], reverse=True)
process_nodes = []
for line in lines:
	source, destinations = line.replace(' ','').strip().split('->')

	name =  source[1:] if source[0] in  ['%', '&'] else source
	name_indx = get_name_indx(name)
	destinations = [get_name_indx(d) for d in destinations.split(',')]

	if source[0] == '%':
		ctype = CTYPE['FLIPFLOP']		# Flip flop
		state = [0]
	elif source[0] == '&':
		ctype = CTYPE['CONJUNCTION']			# Conjunction
		state = [0]
	else:
		ctype = CTYPE['BROADCASTER']
		state = []

	node = {'name':name_indx,'type':ctype, 'dests':destinations, 'sources':[], 'state':state}
	process_nodes.append(node)

# Sort process nodes by name so array indexing can be used
process_nodes.sort(key=lambda x: x['name'], reverse=False)

# Make sure there is an array entry for every node
for cnt in range(len(nameList)):
	if cnt >= len(process_nodes) or process_nodes[cnt]['name'] != cnt:
		newnode = {'name': cnt, 'type': CTYPE.NONE, 'dests': [], 'sources': [], 'state': []}
		process_nodes.insert(cnt, newnode)
		# process_nodes.sort(key=lambda x: x['name'], reverse=False)

# Now loop through the process nodes and update the sources for the CONJUNCTION modules
for node in process_nodes:
	dests = node['dests']
	for d in dests:
		if process_nodes[d]['type']==CTYPE.CONJUNCTION:
			if node['name'] not in process_nodes[d]['sources']:
				process_nodes[d]['sources'].append(node['name'])
				process_nodes[d]['sources'].sort()
			process_nodes[d]['state'] = [0]*len(process_nodes[d]['sources'])

# Now process 1000 button presses
total_signals = (0,0)
for _ in range(1000):
	num_signals = run_process(process_nodes)
	# print(f'{num_signals}\n')
	total_signals = (num_signals[0]+total_signals[0], num_signals[1]+total_signals[1])

print(f'Part 1: {total_signals}')
print(f'Part 1: cumulative {total_signals[0]*total_signals[1]}\n')

##############
# Part 2  Find number of button pressses until 'rx' receives a single low pulse
# ############
# Non General solution:  Following pattern of previous problems assume the 4 CONJUNCTIONS feeding the
# output are periodic and the number presses is the LCM of the first press of each of these 4
#############
# RX is a conjunction: Find the number times for a 1 in each of the 4 component signals
# then use LCM in math
##############
def zero_states(process_nodes):
	for node in process_nodes:
		if node['type'] == CTYPE.FLIPFLOP:
			node['state'][0] = 0
		elif node['type'] == CTYPE.CONJUNCTION:
			node['state'] = [0]*len(node['state'])

# Find the 4 processes that feed the conjunction 'rm' that feeds 'rx'
# All four must be high at same time to output 0 to 'rx'
target_indices = (11,13,22,27)
first_1 = [0, 0, 0, 0]
button_presses = 0
for cnt in range(len(target_indices)):
	target_indx =  target_indices[cnt]
	zero_states(process_nodes);
	target_found=False
	button_presses = 0
	while (not target_found):
		button_presses += 1
		num_signals = run_process(process_nodes,target_indx)
		if not button_presses%10000:
			print(f'{button_presses}')
	first_1[cnt] = button_presses


from math import lcm
first_rx = lcm(*first_1)

print(f'Part2: {first_1}')
print(f'Part2: {first_rx}')
