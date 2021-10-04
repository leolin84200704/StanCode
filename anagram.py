"""
File: anagram.py
Name:
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

import time                   # This file allows you to calculate the speed of your algorithm

# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop
dictionary = []               # Read all the words in the dictionary
count = 0                     # Count how many anagrams did the program found


def main():
    global count
    """
    This program allows user to find all the combination of a set of characters that exists in the dictionary.
    """
    read_dictionary()

    ####################
    print('Welcome to stanCode "Anagram Generator" (or -1 to quit)')
    while True:
        count = 0
        word = input('Find anagrams for: ')
        start = time.time()
        if word == EXIT:
            break
        else:
            find_anagrams(word)
            end = time.time()
            print('----------------------------------')
            print(f'The speed of your anagram algorithm: {end - start} seconds.')
    ####################


def read_dictionary():
    """
    This function reads file "dictionary.txt" stored in FILE and appends words in each line into a Python list.
    """
    with open(FILE, 'r') as f:

        for line in f:
            dictionary.append(line[:-1])


def find_anagrams(s):
    """
    lst: (list) This list contains all the characters that the user insert
    lst2: (list) This list contains all the character combinations that have already been searched
    lst3: (list) This List contains all the words that are found in the dictionary
    """
    lst = []
    lst2 = []
    lst3 = []
    for i in range(len(s)):
        lst.append(s[i])
    print("Searching...")
    find_anagrams_helper(lst, [], len(lst), lst2, lst3)
    print(str(count) + " anagrams: " + str(lst3))


def find_anagrams_helper(lst, current_s, number, lst2, lst3):
    """
    lst: (list) This list contains all the characters that the user insert
    current_s: (list) the list of characters that the program is examining
    number: (variable) the length of the word that the user insert
    lst2: (list) This list contains all the character combinations that have already been searched
    lst3: (list) This List contains all the words that are found in the dictionary
    """
    global count
    if len(current_s) == number:
        if ''.join(current_s) in dictionary:
            print(f"Found: {''.join(current_s)}")
            print("Searching...")
            lst3.append(''.join(current_s))
            count += 1
            return
    else:
        if len(current_s) > 1 and not has_prefix(current_s):
            return
        else:
            for i in range(len(lst)):
                # Choose
                current_s += lst[i]
                lst.pop(i)
                # Explore
                if "".join(current_s) not in lst2:
                    find_anagrams_helper(lst, current_s, number, lst2, lst3)
                    lst2.append("".join(current_s))
                # Un-choose
                ch = current_s.pop()
                lst.insert(i, ch)


def has_prefix(sub_s):
    """
    If there are words in the dictionary that starts with sub_s, this object will return True. Otherwise, the program
    will return false.
    sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
    """
    for word in dictionary:
        if "".join(word).startswith("".join(sub_s)) is True:
            return True
    return False

if __name__ == '__main__':
    main()
