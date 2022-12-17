"""
Author: Umidjon Muzrapov
Class: CS 120
File: maze_solver.py
Purpose: The program solves a maze.
It reads the map up from a file, builds a tree to represent
the maze, and then searches through the tree to find a
path from the start to the end.
"""


class MazeNode:
    """
    This class represents a maze node, or a single element
    of the maze. It can contain the references to unlimited number of nodes.
    It also contains value as well as x and y coordinates of the maze element.

    The constructor builds a maze node without any connection to
    other nodes, which can be added later. The value, x and y
    coordinates should be given to initialize the object.

    The class has 2 public attributes:
        val: can be #, S or E
        connections: list that can hold unlimited references to other nodes.
        It is pre-set to hold 4. The user can add more nodes later on
        by calling a simple method of the class.


    The class has 2 methods:
        get_coordinates(self): return x and y as a tuple.
        add_more_connection: adds a connection in addition to
        4 pre-existing connections if needed.

    """

    def __init__(self, x, y, val):
        self.val = val
        self.__x = x
        self.__y = y
        self.connections = [None, None, None, None]

    def get_coordinates(self):
        """
        The function returns the x and y
        values of the node as a tuple.
        
        :return: a tuple

        Pre-condition: None
        """
        return self.__x, self.__y

    def add_more_connection(self, node):
        """
        This function adds additional connection
        to the node if needed.

        :param node: maze node object.
        :return:  None

        Pre-condition: None
        """
        self.connections.append(node)


def process_maze():
    """
    This function reads a text file holding a maze.
    It processes maze. If the maze meets the criteria,
    the function returns True as well as a list of tuples
    representing maze and its 2-D list copy.

    :return:
    Boolean: shows if the maze is found and meets the criteria.
    maze: a list of tuple that represents the maze.
    maze_copy: a list of lists that represents the maze.

    Pre-condition:None
    """
    maze = []
    maze_copy = []

    try:
        in_file = input()
        in_file = open(in_file, 'r')

        for line in in_file:
            line = line.rstrip('\n')
            line = list(line)
            # use tuple because maze should not change.
            maze.append(tuple(line))
            maze_copy.append(line)

        go_on = check_map(maze)
        return go_on, maze, maze_copy

    except FileNotFoundError:  # maze text does not exist.
        print(f"ERROR: Could not open file: {in_file}")
        return False, maze, maze_copy


def check_map(maze):
    """
    This function  makes sure that
    the maze has only allowed characters.
    If it has extra character, the code will display
    an error message.

    :param maze: a list of tuples representing the maze.
    :return:
    go_on: Boolean that tells if the maze passes the tests and
    has the right format.

    Pre-condition: None
    """
    s_count = 0
    e_count = 0
    allowed_list = ['#', 'S', 'E', ' ']

    for line in maze:
        for char in line:

            if char not in allowed_list:
                print('ERROR: Invalid character in the map')
                return False

            if char == 'S':
                s_count += 1

            if char == 'E':
                e_count += 1

    go_on = check_start_end(s_count, e_count)
    return go_on


def check_start_end(s_count, e_count):
    """
    This function is a part of maze checking functions.
    It makes sure that the maze has exactly one END and START.
    If no, it gives the appropriate error message.

    :param s_count: the numbers of 'starts' in maze
    :param e_count: the number of 'end' in maze
    :return:
    Boolean: True if the maze has only one end and start.
    False, otherwise.

    Pre-condition: None
    """
    if s_count > 1:
        print('ERROR: The map has more than one START position')
        return False

    if e_count > 1:
        print('ERROR: The map has more than one END position')
        return False

    if s_count == 0 or e_count == 0:
        print('ERROR: Every map needs exactly one START and'
              ' exactly one END position')
        return False

    return True


def get_cells(maze):
    """
    This function gets the (x, y) coordinates of
    each element in maze. In returns a list
    of all coordinates as a list of tuples as well as
    x and y coordinates of the start coordinates.

    :param maze: a list of tuples representing the maze.
    :return:
    coordinates_list: a list of tuples
      representing the coordinates of maze elements.
    start_coordinates[0]: x coordinate of the start point.
    start_coordinates[1]: y coordinate of the start point.

    Pre-condition: None
    """
    coordinates_list = []
    allowed = ['#', 'S', 'E']  # ignore spaces.

    for y in range(len(maze)):
        for x in range(len(maze[y])):

            if maze[y][x] in allowed:
                coordinates_list.append((x, y))

            if maze[y][x] == 'S':
                start_coordinates = [x, y]

    return sorted(set(coordinates_list)), \
           start_coordinates[0], start_coordinates[1]


def build_tree(x, y, maze):
    """
    The function builds a tree recursively.

    :param x: x coordinate of the maze.
    :param y: y coordinate of the maze.
    :param maze: 2-d list representing the maze.
    :return: the root that refers to the whole tree.

    Pre-condition: None
    """
    root = MazeNode(x, y, maze[y][x])
    # change the original maze to avoid going to the parent.
    maze[y][x] = " "

    # conditional block checks if moving up, down, left and right is possible.
    if y - 1 >= 0 and x < len(maze[y - 1]) and maze[y - 1][x] != ' ':
        root.connections[0] = build_tree(x, y - 1, maze)

    if y + 1 < len(maze) and x < len(maze[y + 1]) and maze[y + 1][x] != ' ':
        root.connections[1] = build_tree(x, y + 1, maze)

    if x - 1 >= 0 and maze[y][x - 1] != ' ':
        root.connections[2] = build_tree(x - 1, y, maze)

    if x + 1 < len(maze[y]) and maze[y][x + 1] != ' ':
        root.connections[3] = build_tree(x + 1, y, maze)

    return root


def search_tree(root, path):
    """
    The function iterates through the
    tree, getting a solution path to the maze.

    :param root: object that refers to the whole tree
    :param path: list that refers to the solution path.
    :return:
    Boolean: True if the E is found.

    Pre-condition: None
    """

    if root is None:
        return False

    path.append(root.get_coordinates())

    if root.val == 'E':
        return True

    if search_tree(root.connections[0], path) or \
            search_tree(root.connections[1], path) or \
            search_tree(root.connections[2], path) or\
            search_tree(root.connections[3], path):
        return True

    path.pop(-1)

    return False


def print_coordinates(maze, coordinates_list):
    """
    This functions prints out the cordinates
    of the maze elements one per line.

    :param maze: a list that represents a maze.
    :param coordinates_list: sorted list.
    :return: None

    Pre-condition: None
    """
    print('DUMPING OUT ALL CELLS FROM THE MAZE:')
    for element in coordinates_list:

        if maze[element[1]][element[0]] == "E":
            print(element, f"    END")

        elif maze[element[1]][element[0]] == "S":
            print(element, f"    START")

        else:
            print(element)


def print_tree(root, space=''):
    """
    This function prints a tree in pre-order:
    root, up, down, left, right.

    :param root: a node that refers to the whole tree.
    :param space: some space to build a tree structure.
    :return:  None

    Pre-condition: None
    """

    if root is None:
        return None

    print(space + str(root.get_coordinates()))
    print_tree(root.connections[0], space + '|')
    print_tree(root.connections[1], space + '|')
    print_tree(root.connections[2], space + '|')
    print_tree(root.connections[3], space + '|')


def print_path(path):
    """
    This function prints the solution path.
    One coordinate per line.

    :param path: a list of tuples that represent
     coordinates of solution.
    :return: None

    Pre-condition: None
    """
    print('PATH OF THE SOLUTION:')
    for element in path:
        print(element)


def dump_size(cells):
    """
    This function displays the width and height
    of the maze.

    :param cells: a list of tuples
      representing the coordinates of maze elements.
    :return: None

    Pre-condition: None
    """
    width = max(cells, key=lambda item: item[0])
    height = max(cells, key=lambda item: item[1])
    print('MAP SIZE:')
    print(f'  wid: {width[0] + 1}')
    print(f'  hei: {height[1] + 1}')


def show_path(maze, path):
    """
    This function displays the maze with
    the solution highlighted with dots.

    :param maze: a list of tuple that represent the maze.
    :param path: a list of tuples that represent coordinates
    of solution.
    :return: None

    Pre-condition: None
    """
    print('SOLUTION:')
    maze_copy = []

    # convert tuples to list.
    for line in maze:
        line = list(line)
        maze_copy.append(line)

    for element in path[1:-1]:
        maze_copy[element[1]][element[0]] = '.'

    for line in maze_copy:
        print(''.join(line))


def process_command(maze, cells, root, path):
    """
    This functions simply processes the command.
    Based on the command, it calls the right function.

    :param maze: a list of tuple that represent the maze.
    :param cells: a list of tuples
      representing the coordinates of maze elements.
    :param root: a node that reference the whole tree
    :param path: a list of tuples that represent coordinates
    of solution.
    :return: None

    Pre-condition: None
    """
    command = input()

    if command == 'dumpTree':
        print('DUMPING OUT THE TREE THAT REPRESENTS THE MAZE:')
        print_tree(root, space='')

    elif command == 'dumpCells':
        print_coordinates(maze, cells)

    elif command == 'dumpSolution':
        print_path(path)

    elif command == 'dumpSize':
        dump_size(cells)

    elif command == '':
        show_path(maze, path)

    else:
        print('ERROR: Unrecognized command NOT_A_VALID_COMMAND')


def main():
    # check the format of maze and convert it into a list.
    go_on, maze, maze_copy = process_maze()

    if go_on:
        cells, x, y = get_cells(maze)
        root = build_tree(x, y, maze_copy)
        path = []  # will hold the solution path
        search_tree(root, path)

        process_command(maze, cells, root, path)


main()
