"""

File: railyard.py
Author: Umidjon Muzrapov
Course: CSS 120
Purpose: The program reads the commands
(move int int int or quit) from the user
and displays the state of the game
each time after the command is processed.
The game ends if the user commands to quit or
the no locomotive left.
"""


def create_railyard(in_file):
    """
    This function creates a list that represents
    the railyard.
    :param in_file: string, the name of railyard txt file.
    :return: list that represent railyard
    Pre-conditions: None
    """
    try:
        in_file = open(in_file, 'r')
        railyard = []
        for line in in_file:
            line = list(line.rstrip('\n'))
            railyard.append(line)

        return railyard

    # what to do if file is not found.
    except FileNotFoundError:
        print('ERROR: Could not open the yard file')
        railyard = 'no file'
        return railyard


def rail_printer(railyard):
    """
    This function displays the railyard in text format
    and also shows the number of locomotive and destinations.
    :param railyard: list that represent railyard
    :return: integer that represents numbers of locomotives.
    Pre-conditions: None
    """
    locomotive_count = 0
    my_set = set()
    count = 1
    for track in railyard:
        track = ''.join(track)
        print(f'{count}: {track}')
        count += 1
        my_set.update(list(track))
        if 'T' in track:
            locomotive_count += 1
    print(f'Locomotive count:  {locomotive_count}')

    if locomotive_count > 0:
        print(f'Destination count: {len(my_set) - 2}')

    elif locomotive_count == 0:
        print(f'Destination count: {len(my_set) - 1}')

    return locomotive_count


def check_number_type(command):
    """
    This function makes sure that 2nd-4th
    elements of the move command are integers.
    :param command: a list that represents the move command
    :return: 
    all_elements_integer: Boolean, true if all elements are int.
    message: string that shows which element is not int.
    Pre-conditions: None
    """
    all_elements_integer = True
    message = "Good"
    count = 1
    for element in command[1:]:

        if element.isalpha() or not float(element).is_integer():
            all_elements_integer = False
            if count == 1:
                message = f"ERROR: Could not convert the " \
                          f"'count' value to an integer: '{command[1]}'"

            elif count == 2:
                message = f"ERROR: Could not convert the " \
                          f"'from-track' value to an integer: '{command[2]}'"

            elif count == 3:
                message = f"ERROR: Could not convert the" \
                f" 'to-track' value to an integer: '{command[3]}'"

            return all_elements_integer, message

        count += 1

    return all_elements_integer, message


def check_command(command, railyard):
    """
    This function checks the format of the command:
    if it is allowed commend and the number of parameters.
    If the command is move, it also ensures that to and from tracks
    are not same and numbers including car number are not negative.
    :param command: a list that represents command
    :param railyard: list that represent railyard
    :return:
    validity -- Boolean that represents if the move is valid.
    message --  says why the move is invalid.
    Pre-conditions: We need to return only error oen error message,
    whoever error comes first.
    """
    commands = ['move', 'quit']
    error_message_format = "ERROR: The only valid command" \
                           " formats are (where each X represents an integer):"
    if command[0] not in commands:  # check if the command is valid.
        message = f'''{error_message_format}
move X X X
quit\n
        '''
        validity = False
        return validity, message

    elif (len(command) != 4 and command[0] == 'move') or \
            (len(command) != 1 and command[0] == 'quit'):
        validity = False
        message = f'''{error_message_format}
move X X X
quit \n '''
        return validity, message

    # checks tha move command is valid.
    elif command[0] == 'move':
        # the separate function checks if all elements are integers.
        all_elements_integer, message_int = check_number_type(command)
        if not all_elements_integer:
            message = message_int + '\n'
            validity = False

            return validity, message

        elif command[2] == command[3]:
            validity = False
            message = "ERROR: The 'to' track is the same as the 'from' track."
            return validity, message

        elif int(command[2]) <= 0 or int(command[3]) <= 0 or int(command[2]) \
                > len(railyard) or int(command[3]) > len(railyard):
            validity = False
            message = f"ERROR: The to-track or from-track number is invalid."
            return validity, message

        elif int(command[1]) < 0:
            validity = False
            message = 'ERROR: Cannot move a negative number of cars.'
            return validity, message
        # if all possible errors are passed, validity is True.
        else:
            validity = True
            message = "Good"
            return validity, message
    # Need this to ensure that two values are always returned.
    else:
        validity = True
        message = "Good"
        return validity, message


def process_command(command, railyard):
    """
    This function realizes the move or quit command.
    :param command: the list that represent command
    :param railyard: the lsit that represents the railyard
    :return: 
    go_on: Boolean -- used to know if the program should go on.
    cars_together: a list of cars
    Pre-condition: the command is checked, and it is alright.
    """
    command_type = command[0]
    if command_type == 'move':
        cars_together = process_move(command, railyard)
        go_on = True

    else:
        go_on = False
        cars_together = 'We are quitting'

    return go_on, cars_together


def process_move(command, railyard):
    """
    If the command is move and valid, this function
    checks if the move is possible. If so, it orders to
    realize the actual move.
    :param command: the list representing the command
    :param railyard: lsit representing the railyard
    :return: cars_together -- the list of cars that we have on to
    track after the movement.
    Pre-condition: None
    """
    valid_move, message = check_move(command, railyard)
    if valid_move:
        cars_together = realize_move(command, railyard)

    else:
        print(message)
        cars_together = 'No cars since move is invalid'

    return cars_together


def realize_move(command, railyard):
    """
    This function moves the elements of the railyard to
    realize the move command.
    :param command: the list that represents the command.
    :param railyard: the list that represents the railyard.
    :return: cars_together: the list of cars that we have on to
    track after the movement.
    Pre-condition: None
    """
    print(f'The locomotive on track {command[2]}'
          f' moved {command[1]} cars to track {command[3]}.')
    print(' ')
    from_tack = int(command[2]) - 1  # index of the from tack.
    to_track = int(command[3]) - 1  # index of to track.
    cars_lst_to = [element for element in railyard[to_track]
                   if element.isalpha if element != 'T' if element != '-']

    from_cars_that_move = []  # cars that should move.
    # add car to the from_cars_that_move list and insert'-' in original lst.
    for i in range(-2, -(int(command[1]) + 1 + 2), -1):
        from_cars_that_move.insert(0, railyard[from_tack][i])
        railyard[from_tack][i] = '-'

    # Take last '-' and add the add.
    # separate the cars and empty spaces, and put cars at the end.
    railyard[from_tack].pop()
    car_left = [element for element in railyard[from_tack] if element != '-']
    spaces = [element for element in railyard[from_tack] if element == '-']
    new_from_track = spaces + car_left
    railyard[from_tack] = new_from_track
    railyard[from_tack].append('-')

    # Insets the cars into to track.
    railyard[to_track] = list(len(railyard[to_track]) * '-')
    cars_together = list(cars_lst_to + from_cars_that_move)
    for i in range(-2, -(len(cars_together) + 2), -1):
        railyard[to_track][i] = cars_together[i + 1]

    return cars_together


def check_move(command, railyard):
    """
    This function checks if the move can actually be realzied
    -- if there is enough space, enough, and if from and to
    tracks have locomotives.
    :param command: the list represents command.
    :param railyard: the list represents the railyard.
    :return:
    validity -- Boolean that represents if the command move is valid.
    message -- string that is error message.
    Pre-condition: None
    """
    from_tack = int(command[2]) - 1  # index of from track.
    to_track = int(command[3]) - 1  # index of to track.
    cars_lst_from = [element for element in railyard[from_tack]
                     if element.isalpha if element != 'T' if element != '-']
    cars_lst_to = [element for element in railyard[to_track]
                   if element.isalpha if element != 'T' if element != '-']
    number_cars_from = len(cars_lst_from)
    # the actual capacity of the to track.
    space_to_track = len(railyard[to_track]) - 2
    available_space_to = space_to_track - len(cars_lst_to)

    if 'T' not in railyard[from_tack]:
        validity = False
        message = f"ERROR: Cannot move from track" \
                  f" {from_tack + 1} because it doesn't have a locomotive."

        return validity, message

    elif 'T' in railyard[to_track]:
        validity = False
        message = f"ERROR: Cannot move to track" \
                  f" {to_track + 1} because it already has a locomotive."

        return validity, message

    elif number_cars_from < int(command[1]):
        validity = False
        message = f"ERROR: Cannot move {command[1]}" \
                  f" cars from track {from_tack + 1}" \
                  f" because it doesn't have that many cars."

        return validity, message

    elif available_space_to < int(command[1]) + 1:
        validity = False
        message = f"ERROR: Cannot move {command[1]}" \
                  f" cars to track {to_track + 1}" \
                  f" because it doesn't have enough space."

        return validity, message

    else:
        validity = True
        message = "Good"
        return validity, message


def depart(railyard, command, cars_together):
    """
    This function empties the line if there is a locomotive
    with all cars going to the same direction.
    :param railyard: list that represent the railayrd
    :param command: list representing the command
    :param cars_together: the list of cars that we have on to
    track after the movement.
    :return: None
    Pre-condition: None
    """
    for i in range(len(railyard)):  # for each track
        track_cars = [element for element in railyard[i] if element.isalpha
                      if element != 'T' if element != '-']
        my_set = set(track_cars)  # set of destinations.

        #  moves only if it has the locomotive and cars.
        if len(track_cars) >= 0 and len(my_set) == 1 and 'T' in railyard[i]:
            count = 1
            # prints the railyard before departure.
            for track in railyard:
                track = ''.join(track)
                print(f"{count}: {track}")
                count += 1
            print(
                f'*** ALERT***  The train on track {command[3]},'
                f' which had {len(cars_together) - 1} cars,'
                f' departs for destination {my_set.pop()}.')
            print('')

            railyard[i] = list(len(railyard[i]) * '-')
            locomotive_count = 0

            for track in railyard:
                if 'T' in track:
                    locomotive_count += 1
            # what to do if no loco left.
            if locomotive_count == 0:
                print('The last locomotive has departed!')
                print('')


def main():
    print('Please give the yard file:')
    in_file = input()
    railyard = create_railyard(in_file)

    # We go further only if the yard file exists.
    if railyard != 'no file':
        rail_printer(railyard)

        go_on = True
        locomotive = 1  # used to know when there is no loc lef.
        # keeps asking for the command until asked to quit.
        while go_on and locomotive > 0:
            command = input()
            print('')
            print('What is your next command?')
            print(' ')
            command = command.split()

            validity, message = check_command(command, railyard)
            if validity:
                # checks the moves command and realize the move.
                go_on, cars_together = process_command(command, railyard)

                if go_on:
                    depart(railyard, command, cars_together)
                    locomotive = rail_printer(railyard)

                if not go_on:
                    print('Quitting!')

            else:  # What error has occurred.
                print(message)
                go_on = True
                rail_printer(railyard)

        print(" ")


main()
