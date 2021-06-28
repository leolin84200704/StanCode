"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import sys


def add_data_for_name(name_data, year, rank, name):
    """
    Adds the given year and rank to the associated name in the name_data dict.

    Input:
        name_data (dict): dict holding baby name data
        year (str): the year of the data entry to add
        rank (str): the rank of the data entry to add
        name (str): the name of the data entry to add

    Output:
        This function modifies the name_data dict to store the provided
        name, year, and rank. This function does not return any values.

    """
    if name not in name_data:                           # If the name is not in d, then add one in the d dictionary.
        name_data[name] = {}
    if year not in name_data[name]:                     # If the year is not in name,
        name_data[name][year] = rank                    # then add one in the d dictionary.
    elif int(name_data[name][year]) > int(rank):        # If the rank in the exact year is smaller than the old one,
        name_data[name][year] = rank                    # switch the rank in the year with the new one.


def add_file(name_data, filename):
    """
    Reads the information from the specified file and populates the name_data
    dict with the data found in the file.

    Input:
        name_data (dict): dict holding baby name data
        filename (str): name of the file holding baby name data

    Output:
        This function modifies the name_data dict to store information from
        the provided file name. This function does not return any value.

    """
    with open(filename, 'r') as f:
        # If it is the first line that the program reads, the program gets the string "year"
        first_time = True
        for line in f:
            if first_time:
                first_time = False
                year = "".join(line.split())
        # If not, the program gets rank, name1 and name2 accordingly, then feed the data to the dictionary "name_data".
            else:
                split = line.split(',')
                rank = split[0]
                rank = "".join(rank.split())
                name1 = split[1]
                name1 = "".join(name1.split())
                add_data_for_name(name_data, year, rank, name1)
                name2 = split[2]
                name2 = "".join(name2.split())
                add_data_for_name(name_data, year, rank, name2)


def read_files(filenames):
    """
    Reads the data from all files specified in the provided list
    into a single name_data dict and then returns that dict.

    Input:
        filenames (List[str]): a list of filenames containing baby name data

    Returns:
        name_data (dict): the dict storing all baby name data in a structured manner
    """
    # Create an empty dictionary called name_data, and have all the data in "filenames" add in the dictionary.
    name_data = {}
    for filename in filenames:
        add_file(name_data, filename)
    return name_data


def search_names(name_data, target):
    """
    Given a name_data dict that stores baby name information and a target string,
    returns a list of all names in the dict that contain the target string. This
    function should be case-insensitive with respect to the target string.

    Input:
        name_data (dict): a dict containing baby name data organized by name
        target (str): a string to look for in the names contained within name_data

    Returns:
        matching_names (List[str]): a list of all names from name_data that contain
                                    the target string

    """
    # If the user is searching name in the "search" section, then this object will search all the names
    # that are longer or equal length with the target.
    # And compare the name and the target character by character.
    # The program returns every name in the namelist that contains the "target" part.
    names = []
    for name in name_data:
        # If the target is longer than the name, the object will pass the name.
        if len(name) >= len(target):
            name_length = len(name)
            target_length = len(target)
            # The object will only compare the target and the name from the first character of the name
            # to the "name_length - target_length + 1"th character, moving one character backward
            # will make the target longer than the remaining character, so there will be no need to test.
            for i in range(name_length - target_length + 1):
                count = 0
                for j in range(target_length):
                    if str.lower(name[i+j]) == str.lower(target[j]):
                        count += 1
                # If count equals the number of characters in target, that means the all characters in target
                # matches the name we look up in the exact same order.
                if target_length == count:
                    if name not in names:
                        names.append(name)
    return names


def print_names(name_data):
    """
    (provided, DO NOT MODIFY)
    Given a name_data dict, print out all its data, one name per line.
    The names are printed in alphabetical order,
    with the corresponding years data displayed in increasing order.

    Input:
        name_data (dict): a dict containing baby name data organized by name
    Returns:
        This function does not return anything
    """
    for key, value in sorted(name_data.items()):
        print(key, sorted(value.items()))


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # Two command line forms
    # 1. file1 file2 file3 ..
    # 2. -search target file1 file2 file3 ..

    # Assume no search, so list of filenames to read
    # is the args list
    filenames = args

    # Check if we are doing search, set target variable
    target = ''
    if len(args) >= 2 and args[0] == '-search':
        target = args[1]
        filenames = args[2:]  # Update filenames to skip first 2

    # Read in all the filenames: baby-1990.txt, baby-2000.txt, ...
    names = read_files(filenames)

    # Either we do a search or just print everything.
    if len(target) > 0:
        search_results = search_names(names, target)
        for name in search_results:
            print(name)
    else:
        print_names(names)


if __name__ == '__main__':
    main()
