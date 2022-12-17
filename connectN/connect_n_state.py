class Connect_N_State:
    """
    This class represents the current state of the game.
    It can contain the board of the size up to 10x10 and
    up to 5 players. Using it the user, can also get
    the name of the user, players, target and current player,
    and perform various operations (look at the methods).

    The class does not have any public attributes.

    The class has the following list of methods:
        get_size(): returns the size of the board
        get_target(): gets the target
        get_player_list(): returns the list of players.
        is_game_over(): checks if the game is over
        get_winner(): tells the name of the winner
        is_board_full(): checks if the board is full.
        is_column_full(col): checks if the given c. is full.
        get_cell(x,y): gets the value at cell (x,y)
        get_cur_player(): tells whose turn to play
        move(col): drops the token at specified col.
        print(): prints the board

    The constructor builds an empty board, where an empty cell
    is represented by '.'. One must pass width and height
    of the board, the target size, a list of players,
    It also stores the current player and the board.
    """
    def __init__(self, wid, hei, target, players):
        self._width = wid
        self._height = hei
        self._target = target
        self._players = players
        self._board = [['.'] * self._width for i in range(self._height)]
        self._cur = self._players[0]

    def is_target_hit(self):
        """
        This method checks if the target has been hit.
        :return: Boolean -- True if the target is hit.
        Pre-condition: None
        """
        if self.is_target_found():
            return True

        else:
            return False

    def is_board_full(self):
        """
        This method checks if the board is full.
        :return: Boolean, True if the board is full.
        Pre-condition: None
        """
        for inner_lst in self._board:
            for element in inner_lst:

                if element == '.':  # . means there is empty spot.
                    return False

        return True

    def is_game_over(self):
        """
        It checks if the game is over. It is over if the board
        is full or there the target is hit.
        :return: Boolean, True if the game is over.
        Pre-condition: None
        """
        if self.is_target_hit() or self.is_board_full():
            return True
        else:
            return False

    def is_column_full(self, col):
        """
        This method checks if the column the player chooses
        has some empty space.
        :param col:integer that shows to which column the piece
        should go
        :return:Boolean, True if the column is full.
        Pre-condition: col in range of height
        """
        for i in range(-1, -self._height - 1, -1):
            if self._board[i][col] == '.':
                return False

        return True

    def move(self, col):
        """
        This method realizes the actual move if there
        is place in the column. False if fails.
        :param col:integer that shows to which column the piece
        :return: Boolean if the move was successful.
        Pre-condition: None
        """
        # Check if the is some space in the column chosen.
        if not self.is_column_full(col):
            # This block puts the element in the first available spot.
            for i in range(-1, -self._height - 1, -1):
                if self._board[i][col] == '.':
                    self._board[i][col] = self._cur

                    # Changes the current player appropriately.
                    index_cur = self._players.index(self._cur)
                    if index_cur < len(self._players) - 1:
                        self._cur = self._players[index_cur + 1]
                    else:
                        self._cur = self._players[0]

                    return True

            return False

    def get_cur_player(self):
        """
        This method return the current player.
        :return: string the name of the current player
        Pre-condition: None
        """
        return self._cur

    def get_cell(self, x, y):
        """
        This method gets the cell value from the board when
        the user keys x and y coordinates.
        :param x: integer shows the x coord of the element
        :param y: integers shows the y coord of the element.
        :return:  string that represent the content fo the cell.
        Pre-condition: x and y are in within the board.
        """
        new_grid = []
        # This block reorders the grid, so that (0,0) is at lower-left side.
        for x_c in range(self._width):
            this_colum = []
            for y_c in range(self._height):
                this_colum.append(self._board[self._height - 1 - y_c][x_c])
            new_grid.append(this_colum)

        # Makes sure to return the right cell from the board..
        dict_letter_word = {element[0]: element for element in self._players}
        if new_grid[x][y] == '.':
            return None

        elif new_grid[x][y] in dict_letter_word:
            return dict_letter_word[new_grid[x][y]]

        else:
            return new_grid[x][y]

    def is_target_found(self):
        """
        This method checks if the target is hit by
        checking the target, eg. YYYY, in all 8
        directions.
        :return: Booliean, True if the target is hit.
        Pre-condition: None
        """
        length = self._target - 1
        found = False
        target = [self._cur] * self._target

        # block sets the right target
        index_letter = self._players.index(target[0])
        if index_letter > 0:
            target = [self._players[index_letter - 1]] * self._target
        else:
            target = [self._players[-1]] * self._target
        # find the possible locations of the players
        player_locations = self.get_player_location(target)

        for location in player_locations:  # checks in each direction.
            needed_parameters = [length, location, self._board, target]
            nd = needed_parameters  # to shorten needed_parameters
            directions = {'E': self.go_east(nd), 'W': self.go_west(nd),
                          'N': self.go_north(nd), 'S': self.go_south(nd),
                          'ES': self.go_es(nd), 'EN': self.go_en(nd),
                          'WN': self.go_wn(nd), 'WS': self.go_ws(nd)}

            for key, value in directions.items():
                go_on = value
                if not go_on:
                    found = True
                    return found
        if not found:
            return False

    def go_east(self, needed_parameters):
        """
        The method tries to locate the target going east direction.
        Pre-condition: Number of elements in each row of grid is the same.
        :param needed_parameters: a list of necessary arguments
        to find the target.
        :return:
        Boolean: False if target is found.
        Pre-condition: None
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

            return False

        else:
            return True

    def go_west(self, needed_parameters):
        """
        The method tries to locate the target going west direction.
        Pre-condition: Number of elements in each row of grid is the same.
        :param needed_parameters: a list of necessary arguments
        to find the target.
        :return:
        Boolean: False if the target is found.
        Pre-condition: None
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

            return False

        else:
            return True

    def go_north(self, needed_parameters):
        """
        The method tries to locate the target going north direction.
        Pre-condition: Number of elements in each row of grid is the same.
        :param needed_parameters: a list of necessary arguments
        to find the target.
        :return:
        Boolean: False if the target is found.
        Pre-condition: None
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

            return False

        else:
            return True

    def go_south(self, needed_parameters):
        """
        The method tries to locate the target going south direction.
        Pre-condition: Number of elements in each row of grid is the same.
        :param needed_parameters: a list of necessary arguments
        to find the target.
        :return:
        Boolean: False if the target is found.
        Pre-condition: None
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

            return False

        else:
            return True

    def go_es(self, needed_parameters):
        """
        The method tries to locate the target going east-south direction.
        Pre-condition: Number of elements in each row of grid is the same.
        :param needed_parameters: a list of necessary arguments
        to find the target.
        :return:
        Boolean: False if the target is found.
        Pre-condition: None
        """
        length = needed_parameters[0]
        grid = needed_parameters[2]
        word = needed_parameters[3]
        row_start = needed_parameters[1][0]
        column_start = needed_parameters[1][1]

        if row_start + length < len(grid)\
                and column_start + length < len(grid[0]):

            for inc in range(length + 1):
                if grid[row_start + inc][column_start + inc] != word[inc]:
                    return True

            return False

        else:
            return True

    def go_en(self, needed_parameters):
        """
        The method tries to locate the target going east-north direction.
        Pre-condition: Number of elements in each row of grid is the same.
        :param needed_parameters: a list of necessary arguments
        to find the target.
        :return:
        Boolean: False if the target is found.
        Pre-condition: None
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

            return False

        else:
            return True

    def go_ws(self, needed_parameters):
        """
        The method tries to locate the target going west-south direction.
        Pre-condition: Number of elements in each row of grid is the same.
        :param needed_parameters: a list of necessary arguments
        to find the target.
        :return:
        Boolean: False if the target is found.
        Pre-condition: None
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

            return False

        else:
            return True

    def go_wn(self, needed_parameters):
        """
        The method tries to locate the target going west-north direction.
        Pre-condition: Number of elements in each row of grid is the same.
        :param needed_parameters: a list of necessary arguments
        to find the target.
        :return: Boolean: False if the target is found.
        Pre-condition: None
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

            return False

        else:
            return True

    def get_winner(self):
        """
        This method gives the winner or None if a tie.
        :return: string that is the name of the winner
        if there is a winner; None if there is a tie.
        Pre-condition: called if game is over
        """
        if not self.is_board_full():
            index_letter = self._players.index(self._cur)

            # black find the winner based on the self._cur
            if index_letter > 0:
                word = self._players[index_letter - 1]
            else:
                word = self._players[-1]

            return word

        else:
            return None

    def print(self):
        """
        This method prints the board. It prints '.' if cell is
        empty and the first letter if otherwise.
        :return: None
        Pre-condition: None
        """
        word_letter = {element: element[0] for element in self._players}
        for in_line in self._board:
            count = 1
            for element in in_line:

                if count < self._width:
                    # need to connect elements in a row.
                    if element in word_letter:
                        print(word_letter[element], end='')
                    else:
                        print('.', end='')

                else:  # prints last element in a row.
                    if element in word_letter:
                        print(word_letter[element])
                    else:
                        print('.')

                count += 1

    def get_player_location(self, target):
        """
        This functions finds the locations of target used
        to check if the target is hit.
        :param target:  string-what the programs checks for.
        :return: a list of tuples, each tuple (row, col).
        Pre-condition: None
        """
        player_locations = []
        letter = target[0]
        for r_numb in range(self._height):
            for c_numb in range(self._width):
                # the location of the first letter is found.
                if self._board[r_numb][c_numb] == letter:
                    player_locations.append((r_numb, c_numb))

        return player_locations

    def get_size(self):
        """
        This method gets the size and returns it in
        a tuple form -- (width, height)
        :return: tuple -- width, height.
        Pre-condition: None
        """
        return (self._width, self._height)

    def get_target(self):
        """
        The method returns how many identical elements
        should be hit -- target.
        :return: integer that represent target.
        Pre-condition: None
        """
        return self._target

    def get_player_list(self):
        """
        The method gets the lsit of players
        :return: list of players.
        Pre-condition: None
        """
        return self._players
