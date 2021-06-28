"""
File: boggle.py
Name: 林宏璠
----------------------------------------
This program allows user to found all the words in the dictionary that can be made up with the connection of the
nearby characters within a 4X4 matrix.
"""

import time

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'		  # This is the filename of an English dictionary
dictionary = []               # Read all the words in the dictionary
count = 0                     # Count how many anagrams did the program found
d = {}						  # This list contains all the characters the user insert
found_ans = []				  # This list contains all the answers that are already found


def main():
	"""
	This program allows user to found all the words in the dictionary that can be made up with the connection of the
	nearby characters within a 4X4 matrix.
	"""
	global found_ans
	read_dictionary()
	for i in range(4):
		lst = input(str(i+1) + " row of letters: ")
		d[i] = lst.lower().split(" ")
		for letter in d[i]:
			if not letter.isalpha() or not len(letter) == 1 or not len(d[i]) == 4:
				print("Illegal Input")
				return 1

	start = time.time()
	####################
	found_ans = []
	# All the 16 characters can be used as the first character of a word.
	for lst in range(4):
		for character in range(4):
			find_anagrams(lst, character)
	print('There are ' + str(count) + ' words in total.')
	####################
	end = time.time()
	print('----------------------------------')
	print(f'The speed of your boggle algorithm: {end - start} seconds.')


def find_anagrams(lst, character):
	"""
	lst: (integer) Which lst (form 0 to 3) is the program examining
	character:  (integer) Which character (form 0 to 3) is the program examining
	"""
	current_s = [d[lst][character]]
	used_position = [lst * 10 + character]
	find_anagrams_helper(lst, character, current_s, used_position)


def find_anagrams_helper(lst, character, current_s, used_position):
	"""
	lst: (integer) Which lst (form 0 to 3) is the program examining
	character:  (integer) Which character (form 0 to 3) is the program examining
	current_s: (list) the list of characters that the program is examining
	used_position: (list) the position of the characters that are already used for a word
					The first character in the first list is recorded as 0
					The second character in the first list is recorded as 1
					The first character in the second list is recorded as 10
					The second character in the second list is recorded as 11
	"""
	if has_prefix(current_s):
		# Finds all the characters nearby and re-run the "look up dictionary" object
		for i in range(-1, 2, 1):
			for j in range(-1, 2, 1):
				# If the range is within the boggle and the character isn't used already
				if 0 <= lst + i <= 3 and 0 <= character + j <= 3 and \
						(lst + i) * 10 + character + j not in used_position:
					# Choose
					used_position.append((lst + i) * 10 + character + j)
					current_s.append(d[lst + i][character + j])
					# Explore
					find_anagrams_helper(lst + i, character + j, current_s, used_position)
					# Un-choose
					used_position.pop()
					current_s.pop()


def read_dictionary():
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""
	with open(FILE, 'r') as f:
		for line in f:
			dictionary.append(line[:-1])


def has_prefix(sub_s):
	"""
	sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	global count, found_ans
	for word in dictionary:
		# Check if there is a word that starts with the combination of the current string
		if "".join(word).startswith("".join(sub_s)) is True:
			# If the word is in the dictionary and the length of the word is equal or longer than 4
			# and the answer is not yet found. The program will print the answer. But will not continue searching
			if len("".join(sub_s)) == len("".join(word)) and len("".join(sub_s)) >= 4 \
					and "".join(sub_s) not in found_ans:
				print(f"Found: {''.join(sub_s)}")
				found_ans .append("".join(sub_s))
				count += 1
			# The program will only continue searching if there is a word in the dictionary that is longer than
			# the current string and starts with the combination of the current string
			else:
				return True
	return False


if __name__ == '__main__':
	main()
