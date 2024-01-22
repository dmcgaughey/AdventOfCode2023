import math
import re


def is_valid(template, code):
  #pdb.set_trace()
  for c in range(len(template)):
    if (template[c]=='#' and code[c]=='.') or (template[c]=='.' and code[c]=='#'):
      return False
  return True


def create_codes(code,indx,numM,vals):
	possible = []
	for val in set(vals):
		for start in range(max([0,indx-(val-numM)-1]),indx+1):
			if start+val+1 >= len(code): break			# Reached the end
			temp_code = list(code)
			temp_code[start] = '.'
			temp_code[start+1:start+val+1] = ['#']*val
			temp_code[start+val+1] = '.'

			code_str = ''.join(temp_code)
			if is_valid(code_str,code):
				possible.append(code_str.replace('..','.'))
	return possible

# noinspection PyUnreachableCode
def find_permutations(code, vals):
	# Use hueristics to find number of permutations given a code and vals list
	code = code.replace('..','.')

	num_N = code.count('#')

	# 0. Stopping criterion
	if not vals and not code:       return 1
	if not vals and num_N == 0:     return 1  	# No values and only ? in remaining code
	if not vals and num_N > 0:      return 0  	# No values left to fit but still # left in code
	if vals and not code:			return 0
	if num_N > sum(vals):           return 0

	# 1a. Find longest '#' in code Add in '.' to make other searches easier
	indx = 0
	while (indx := code.find('#' * max(vals), indx + 1)) >= 0:
		temp_code = list(code)
		if temp_code[indx - 1] == '?': temp_code[indx - 1] = '.'
		if temp_code[indx + max(vals)] == '?': temp_code[indx + max(vals)] = '.'
		code = (''.join(temp_code)).replace('..','.').replace('..','.')

	# 1b Useful constants
	num_spaces = code.count('?') + code.count('#')

	# 2b. Calculate useful values
	perms = 1
	subcodes = code[1:-1].split('.')
	subcodes = [('.' + s + '.') for s in subcodes]
	sub_spaces = [s.count('#') + s.count('?') for s in subcodes]
	sub_N = [s.count('#') for s in subcodes]

	# 2c Stopping criterion based on subblocks
	if num_spaces < sum(vals):		return 0	# Not enough spaces for remaining values
	if len(vals)>len(sub_spaces):			# Check again for sufficent # spaces taking into account need '.' between itens
		if num_spaces -(len(vals)-len(sub_spaces)) < sum(vals):
			return 0
	# if sub_N[0]>vals[0]:				return 0		# Too many #'s in first block for first value

	# 3. (a) # at start of first code or (b) space just big enough for first code and contains '#'
	if code[1] == '#' or (sub_spaces[0]==vals[0] and sub_N[0]>0):
		if code[vals[0] + 1] != '#' and sub_spaces[0]>=vals[0]:
			code = '' if len(code) <= vals[0] + 2 else ('.' + code[vals[0] + 2:])
			perms = 1 * find_permutations(code, vals[1:])
			return perms
		else:
			return 0

	# 3b. Find .?# and length of 1
	if code[1] == '?' and code[2] =='#' and code[3] in ('?','.') and vals[0] == 1:  # Cose of '.?#?' or '.?#?'
		if len(subcodes[0]) < vals[0] + 2: return 0  # Not enough space for code
		code = '' if len(code) < 5 else ('.' + code[4:])
		perms = 1 * find_permutations(code, vals[1:])
		return perms

	# 4. (a) # at end of entire code or (b) space at end is just big enough to hold last term and has 1 or more #
	if code[-2] == '#' or (sub_spaces[-1] ==vals[-1] and sub_N[-1]>0):
		if sub_spaces[-1] < vals[-1] or code[-vals[-1]-2] == '#':
			return 0  # Not enough space for last code
		code = '' if len(code)-2<=vals[-1]+1 else (code[:(-vals[-1] - 2)] + '.')
		# code.replace('..','.')
		perms = 1 * find_permutations(code, vals[:-1])
		return perms


	# 5. All ??? in code
	# 5a. All ?? in code only one val left
	if sub_N[0]==0 and len(sub_N)==1:
		space_needed = sum(vals)+len(vals)-1
		extra_space = sub_spaces[0] - space_needed
		perms = 0 if (extra_space<0) else math.comb(len(vals)+extra_space, len(vals))
		return perms

	# 5b Have just enough space for the code but need to verify it works
	# if len(vals)>len(sub_spaces) and num_spaces -(len(vals)-len(sub_spaces)) == sum(vals):
	# 	if num_N == 0: return 1
	# 	start = 0
	# 	for cnt in range(len(vals)):
	# 		space_needed = sum(vals[:cnt+1]) - len(vals[:cnt+1])

	# 5c. All ??? in code but may fit one or more values (or none)
	if sub_N[0] == 0 and len(sub_N) > 1:
		# Try 0, then 1, then 2, etc subgroups in this space
		perms = 0
		temp_code = code[len(subcodes[0]) - 1:]
		# if len(temp_code)<=2:
		# 	print('here')
		num_vals = len(vals)
		for cnt in range(num_vals+1):
			space_needed = sum(vals[:cnt]) + cnt - 1 if cnt>0 else 0
			extra_space = sub_spaces[0] - space_needed if cnt>0 else 0

			if extra_space<0: return perms

			if len(temp_code) > 2 and vals[cnt:]:
				perms += math.comb(len(vals[:cnt])+extra_space, len(vals[:cnt])) \
						 * find_permutations(temp_code, vals[cnt:])
			elif not vals[cnt:] and temp_code.count('#') == 0:
				# Fit the current code in this block but no more blocks after to process
				perms += math.comb(len(vals[:cnt])+extra_space, len(vals[:cnt]))

		return perms


	# 6. Mixture of # and ? -> trial and error
	# If there is at least 1 # in the first space but not enough room for the first value
	if sub_spaces[0]<vals[0] and sub_N[0]>0: 	return 0

	# 6a. .??#. Just right amount of space for vals[0] but ? at start (no need to search)
	if sub_spaces[0] == vals[0] and sub_N[0] > 0:
		code = '' if len(code) <= vals[0] + 2 else ('.' + code[vals[0] + 2:])
		perms = find_permutations(code, vals[1:])
		return perms

	# 6b.Mixture of # and? and more than one sub_block (accounting for any # in the code)
	if sub_spaces[0]>=vals[0] and sub_N[0]>0:
		perms = 0
		searchObj = re.search(r'#+',code)
		first_indx = searchObj.span()[0] #code.find('#')
		first_numM = len(searchObj.group())

		val_indx = 1
		while val_indx<len(vals) and (sum(vals[:val_indx]) + len(vals[:val_indx])  < first_indx):
			val_indx += 1

		possible = create_codes(code, first_indx, first_numM, vals[:val_indx])
		for pcode in possible:
			perms += find_permutations(pcode, vals)

		return perms

# Debugging Compare with known values from brute force
with open('Dec12CorrectCounts.txt', 'r') as f:
	data = f.readlines()
known = [int(i.strip()) for i in data]
f.close()
print(len(known))

# with open('Dec12test.txt', 'r') as f:
with open('Dec12.txt', 'r') as f:
# with open('Dec12ErrorCodes.txt', 'r') as f:
		lines = f.readlines()

total_correct = 0
correctList = []
error_codes = []
lcnt = 0
# Parse line
for line in lines:
	print(line)
	[code, vals] = line.split()

	# # Special code for Error code file
	# [code, vals, known] = line.split()

	vals = list(map(int, vals.split(',')))
	code = '.' + code + '.'
	code = re.sub(r'[.]+', '.',code)

	# code = '.?.??.??.'
	# vals = [1,1]
	num_correct = find_permutations(code, vals)
	correctList.append(num_correct)
	total_correct += num_correct

	if num_correct != known[lcnt]:
		error_codes.append((code,vals,known[lcnt]))
		print(f'Error {code} {vals} Known {known[lcnt]} Count: {num_correct}')
	lcnt += 1

	# if num_correct != int(known):
	# 	error_codes.append((code, vals, known))
	# 	print(f'Error {code} {vals} Known {known} Count: {num_correct}')

print(f'Total Combinations: {total_correct}')
print(f'Combinations {correctList}')

# f = open('Dec12ErrorCodes2.txt','w')
# for code,vals,known in error_codes:
# 	f.write(f'{code} {vals} {known}\n')
# f.close()

# Part 2:
total_correct = 0
correctList.clear()
for line in lines:
	# print(line)
	[code, vals] = line.split()
	vals = list(map(int, vals.split(',')))
	code = '.' + (code + '?')*4 + code + '.'
	vals = vals * 5
	code = re.sub(r'[.]+', '.',code)
	print(f'Code: {code} {vals}')

	num_correct = find_permutations(code, vals)
	correctList.append(num_correct)
	total_correct += num_correct

print(f'Part 2: Total Combinations: {total_correct}')
print(f'Part 2: Combination {correctList}')
