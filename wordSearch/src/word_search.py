"""
Name of file: word_search.py.
Name of author: Umidjon Muzrapov.
Purpose: The program takes in the file name, which contains crossword
and words we should find. It finds the words in crossword and
prints out each words in separate grid, where everything except
the word is replaced with '.'.
Course: CSS 120.
"""


def get_grid_and_word(in_file):
	"""
	The function processes the file and builds the grid that
	represents crosswords and the list of words.
	Pre-condition: Length of each line in crossword is the same.
	:param in_file: string, the name of the file.
	:return:
	grid: list, our crossword
	word_lst: list, words the code should find.
	"""
	try:
		in_file = open(in_file, 'r')
		line = in_file.readline().rstrip('\n')
		grid = []
		# Builds the crossword.
		while line.rstrip('\n') != '':
			# tuple ensures that the original grid is not deleted.
			line = tuple(line)
			grid.append(line)
			line = in_file.readline().rstrip('\n')
		word_lst = []
		line = in_file.readline().rstrip('\n')

		# Once done with crossword, find the words.
		while line != '':
			word = line
			line = in_file.readline().strip('\n')
			word_lst.append(word)

		return grid, word_lst

	except FileNotFoundError:
		print(" Sorry, the file doesn't exist or cannot be opened")


def get_letter1_locations(grid, word_lst):
	"""
	This function find the first letter locations of each word,
	and build a dictionary, where key is a word, and value is
	a list of locations.
	Pre-condition: Number of elements in each row of grid is
	the same.
	:param grid: a list of tuple, our crossword
	:param word_lst: list, words the code should find.
	:return:
	letter1_dictionary: word-location_list dictionary.
	"""
	letter1_dict = {}
	# Check each letter if it is equal to the first letter.
	for word in word_lst:
		letter1 = word[0]
		letter1_locations = []

		for r_numb in range(len(grid)):
			for c_numb in range(len(grid[0])):
				if grid[r_numb][c_numb] == letter1:
					letter1_locations.append((r_numb, c_numb))

		letter1_dict[word] = letter1_locations

	return letter1_dict


def find_word(grid, word, letter1_locations):
	"""
	The function goes to 8 different directions (E, W, S, N, EN, ES, WS, WN)
	to locate the word. If thw word is found, calls print_grid. If no,
	displays a message that the word was not found.
	Pre-condition: Number of elements in each row of grid is the same.
	:param grid: list, contains lists, a copy of the original grid.
	:param word: string, word that code seeking.
	:param letter1_locations: list of tuples.
	:return: None
	"""
	length = len(word) - 1
	found = False
	#  Checks each location.
	for location in letter1_locations:
		needed_parameters = [length, location, grid, word]
		nd = needed_parameters  # to shorten needed_parameters
		directions = {'E': go_east(nd), 'W': go_west(nd),
					  'N': go_north(nd), 'S': go_south(nd),
					  'ES': go_es(nd), 'EN': go_en(nd), 'WN': go_wn(nd), 'WS': go_ws(nd)}

		for key, value in directions.items():
			go_on = value
			if not go_on:
				print_grid(grid, word, key)
				found = True

	if not found:
		print(f"Word '{word}' not found")


def go_east(needed_parameters):
	"""
	The function tries to locate the word going east direction.
	Pre-condition: Number of elements in each row of grid is the same.
	:param needed_parameters: a list of necessary arguments
	to find the word.
	:return:
	Boolean: False if the word is found.
	"""
	length = needed_parameters[0]
	grid = needed_parameters[2]
	word = needed_parameters[3]
	row_start = needed_parameters[1][0]
	column_start = needed_parameters[1][1]

	if column_start + length < len(grid[0]):

		for col_numb in range(length + 1):
			if grid[row_start][column_start + col_numb] != word[col_numb]:
				return True

		for col_numb in range(length + 1):
			# replace the letters of the found word to make printing easy.
			grid[row_start][column_start + col_numb] = '.'

		return False

	else:
		return True


def go_west(needed_parameters):
	"""
	The function tries to locate the word going west direction.
	Pre-condition: Number of elements in each row of grid is the same.
	:param needed_parameters: a list of necessary arguments
	to find the word.
	:return:
	Boolean: False if the word is found.
	"""
	length = needed_parameters[0]
	grid = needed_parameters[2]
	word = needed_parameters[3]
	row_start = needed_parameters[1][0]
	column_start = needed_parameters[1][1]

	if column_start - length >= 0:

		for col_numb in range(length + 1):
			if grid[row_start][column_start - col_numb] != word[col_numb]:
				return True

		for col_numb in range(length + 1):
			# replace the letters of the found word to make printing easy.
			grid[row_start][column_start - col_numb] = '.'

		return False

	else:
		return True


def go_north(needed_parameters):
	"""
	The function tries to locate the word going north direction.
	Pre-condition: Number of elements in each row of grid is the same.
	:param needed_parameters: a list of necessary arguments
	to find the word.
	:return:
	Boolean: False if the word is found.
	"""
	length = needed_parameters[0]
	grid = needed_parameters[2]
	word = needed_parameters[3]
	row_start = needed_parameters[1][0]
	column_start = needed_parameters[1][1]

	if row_start - length >= 0:

		for row_numb in range(length + 1):
			if grid[row_start - row_numb][column_start] != word[row_numb]:
				return True

		for row_numb in range(length + 1):
			# replace the letters of the found word to make printing easy.
			grid[row_start - row_numb][column_start] = '.'

		return False

	else:
		return True


def go_south(needed_parameters):
	"""
	The function tries to locate the word going south direction.
	Pre-condition: Number of elements in each row of grid is the same.
	:param needed_parameters: a list of necessary arguments
	to find the word.
	:return:
	Boolean: False if the word is found.
	"""
	length = needed_parameters[0]
	grid = needed_parameters[2]
	word = needed_parameters[3]
	row_start = needed_parameters[1][0]
	column_start = needed_parameters[1][1]

	if row_start + length < len(grid):

		for row_numb in range(length + 1):
			if grid[row_start + row_numb][column_start] != word[row_numb]:
				return True

		for row_numb in range(length + 1):
			# replace the letters of the found word to make printing easy.
			grid[row_start + row_numb][column_start] = '.'

		return False

	else:
		return True


def go_es(needed_parameters):
	"""
	The function tries to locate the word going east-south direction.
	Pre-condition: Number of elements in each row of grid is the same.
	:param needed_parameters: a list of necessary arguments
	to find the word.
	:return:
	Boolean: False if the word is found.
	"""
	length = needed_parameters[0]
	grid = needed_parameters[2]
	word = needed_parameters[3]
	row_start = needed_parameters[1][0]
	column_start = needed_parameters[1][1]

	if row_start + length < len(grid) and column_start + length < len(grid[0]):

		for inc in range(length + 1):
			if grid[row_start + inc][column_start + inc] != word[inc]:
				return True

		for inc in range(length + 1):
			# replace the letters of the found word to make printing easy.
			grid[row_start + inc][column_start + inc] = '.'

		return False

	else:
		return True


def go_en(needed_parameters):
	"""
	The function tries to locate the word going east-north direction.
	Pre-condition: Number of elements in each row of grid is the same.
	:param needed_parameters: a list of necessary arguments
	to find the word.
	:return:
	Boolean: False if the word is found.
	"""
	length = needed_parameters[0]
	grid = needed_parameters[2]
	word = needed_parameters[3]
	row_start = needed_parameters[1][0]
	column_start = needed_parameters[1][1]

	if column_start + length < len(grid[0]) and row_start - length >= 0:

		for inc in range(length + 1):
			if grid[row_start - inc][column_start + inc] != word[inc]:
				return True

		for inc in range(length + 1):
			# replace the letters of the found word to make printing easy.
			grid[row_start - inc][column_start + inc] = '.'

		return False

	else:
		return True


def go_ws(needed_parameters):
	"""
	The function tries to locate the word going west-south direction.
	Pre-condition: Number of elements in each row of grid is the same.
	:param needed_parameters: a list of necessary arguments
	to find the word.
	:return:
	Boolean: False if the word is found.
	"""
	length = needed_parameters[0]
	grid = needed_parameters[2]
	word = needed_parameters[3]
	row_start = needed_parameters[1][0]
	column_start = needed_parameters[1][1]

	if column_start - length >= 0 and row_start + length < len(grid):

		for inc in range(length + 1):
			if grid[row_start + inc][column_start - inc] != word[inc]:
				return True

		for inc in range(length + 1):
			# replace the letters of the found word to make printing easy.
			grid[row_start + inc][column_start - inc] = '.'

		return False

	else:
		return True


def go_wn(needed_parameters):
	"""
	The function tries to locate the word going west-north direction.
	Pre-condition: Number of elements in each row of grid is the same.
	:param needed_parameters: a list of necessary arguments
	to find the word.
	:return:
	Boolean: False if the word is found.
	"""
	length = needed_parameters[0]
	grid = needed_parameters[2]
	word = needed_parameters[3]
	row_start = needed_parameters[1][0]
	column_start = needed_parameters[1][1]
	if column_start - length >= 0 and row_start - length >= 0:

		for inc in range(length + 1):
			if grid[row_start - inc][column_start - inc] != word[inc]:
				return True

		for inc in range(length + 1):
			# replace the letters of the found word to make printing easy.
			grid[row_start - inc][column_start - inc] = '.'

		return False

	else:
		return True


def print_grid(grid, word, direction):
	"""
	The function prints the grid, where except for the word,
	everything is replaced with '.'
	:param grid: list, contains lists, a copy of the original grid.
	:param word: string, word the code is seeking.
	:param direction: string.
	:return: None
	"""
	letter_num = 0
	# directions for which the letters come in normal order.
	normal_order_directions = ['E', 'S', 'ES', 'WS']
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if grid[r][c] != '.':
				grid[r][c] = '.'

			else:
				# What to do if the order is normal.
				if direction in normal_order_directions:
					grid[r][c] = word[letter_num]
					letter_num += 1

				# What to do if its reverse.
				else:
					grid[r][c] = word[len(word) - letter_num - 1]
					letter_num += 1
					
	# joins the elements in a row.
	for row in grid:
		print(''.join(row))


def main():
	in_file = input()
	print('Please give the puzzle filename:')
	# Create the crossword and determine the words the code seeks.
	grid, word_lst = get_grid_and_word(in_file)
	# Get the letter_1 locations of the words.
	letter1_dict = get_letter1_locations(grid, word_lst)

	# for each word, create the copy of grid and then find word.
	for word in word_lst:
		new_grid = []
		for inner_element in grid:
			new_grid.append(list(inner_element))

		letter1_locations = letter1_dict[word]
		find_word(new_grid, word, letter1_locations)
		print('')


main()
