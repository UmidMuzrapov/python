"""
File name: ryhmes.py

Name of Author: Umid Muzrapov

Purpose: The program reads words from the user, one word per line.
Then, it returns all the words that perfectly rhyme with the given
word. If no rhyme is found, or word is not in dictionary, program
says there is no word found.

"""


def create_dict():
    """
    The function reads a text file and creates a dictionary.
    It matches word with its pronunciations.
    :return: dictionary that matches word with pronunciations.
    Pre condition: The format of the word and pronunciation is:
    'WORD   PRONUNCIATION'.
    """
    in_file = input("Dictionary you want to use: ")
    in_file = open(in_file, "r")
    pronunciation_dict = {}

    for line in in_file:
        line = line.rstrip('\n').split()

        if line[0] not in pronunciation_dict:
            pronunciation_dict[line[0]] = [line[1:]]

        else:  # adds additional pronunciation.
            # if word is repeated.
            if line[1:] not in pronunciation_dict[line[0]]:
                pronunciation_dict[line[0]].append(line[1:])

    return pronunciation_dict


def get_words():
    """
    It gets words the from the user and format them.
    Create a list of the words to rhyme.
    :return: list of words to find ryhme for.
    Pre-condition:None
    """
    words_lst = []
    word = input()


    while word!='stop':
        word = word.strip()
        words_lst.append(word.upper())

        try:
            word = input()

        except EOFError:
            go_on = False

    return words_lst


def check_condition1(pronunciation):
    """
    The function checks if a word has a primary stress,
    or if the primary stress is on the first phoneme.
    If the word does not pass the test, there are
    no rhymes.
    :param pronunciation: a list of phonemes.
    :return: Boolean that shows if the check went.
    Pre-condition: None
    """
    if '1' not in ''.join(pronunciation) or '1' in pronunciation[0]:
        return False

    else:
        return True


def check_conditions2and3(pronunciation, pronunciation_dict):
    """
    This function checks if the stressed vowel sound
    in both words are identical, as well as any subsequent sounds.
    It also checks if the previous sounds are not same.
    If these conditions are not met, words do not rhyme.
    :param pronunciation: list of phonemes
    :param pronunciation_dict: dictionary of word: [pronunciations]
    :return: dictionary of words that rhyme.
    Pre-condition: None
    """
    match_dict = {}
    for key, value in pronunciation_dict.items():
        for val in value:  # for each pronunciation.

            if check_condition1(val):
                primary_stress1 = [element for element
                                   in pronunciation if '1' in element]
                primary_stress2 = [element for element
                                   in val if '1' in element]
                index_primary1 = pronunciation.index(primary_stress1[0])
                index_primary2 = val.index(primary_stress2[0])

#  primary stresses should be identical.
                if primary_stress1 == primary_stress2:
                    # the rest of sounds should match.
                    if pronunciation[index_primary1:] == val[index_primary2:]:

                        if pronunciation[index_primary1 - 1] \
                                != val[index_primary2 - 1]:
                            match_dict[key] = val

    return match_dict


def print_ryhmes(word, match_dict):
    """
    The function prints rhymes for the word.
    :param word: string
    :param match_dict: dictionary of words that rhyme.
    :return:  None
    Pre-condtion: None
    """
    if len(match_dict) == 0:
        print_not_found(word)

    else:
        print(f'Rhymes for: {word}')
        words = sorted(match_dict.keys())

        for word in words:
            print(f'  {word}')

        print('')


def decide_print(match_dict_general, word, true_list):
    """
    The function decides what to print.
    If all pronunciations do not rhyme,
    print no ryhme is found.
    :param match_dict_general: dictionary, work:[pronunciations]
    :param word: string
    :param true_list: a list that represents if pron.
    has rhymes.
    :return:  None
    Pre-condition: None
    """
    if true_list.count(0) == len(true_list):
        print_not_found(word)

    else:
        print_ryhmes(word, match_dict_general)


def print_not_found(word):
    """
    The message to print if no rhyme is found.
    :param word:  string
    :return:  None
    Pre-condition: None
    """
    print(f"Rhymes for: {word}")
    print('  -- none found --')
    print('\n')


def is_word_meaningful(word):
    """
    The function checks if the given word
    is meaningful.
    :param word: string.
    :return: Boolean.
    True if the word is meaningful.
    Pre-condtion: None
    """
    if word.isspace() or len(word) == 0:
        print('No word given\n')
        return False

    elif len(word.split()) > 1:
        print('Multiple words entered,'
              ' please enter only one word at a time.\n')
        return False

    else:
        return True


def main():
    pronunciaton_dict = create_dict()
    words_lst = get_words()

    for word in words_lst:

        if is_word_meaningful(word):

            try:
                match_dict_general = {}  # ultimate rhyme dictionary
                true_list = []  # use to see if any pronun. works.

                for pronunciation in pronunciaton_dict[word]:
                    
                    if check_condition1(pronunciation):
                        # Check two additional conditions (see the function).
                        match_dict = check_conditions2and3\
                            (pronunciation, pronunciaton_dict)
                        true_list.append(1)
                        match_dict_general = \
                            {**match_dict, **match_dict_general}

                    else:
                        true_list.append(0)

                decide_print(match_dict_general, word, true_list)

            # what to do if the word is not in the dictionary.
            except KeyError:
                print_not_found(word)


main()
