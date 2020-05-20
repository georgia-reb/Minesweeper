# minesweeper_project.py
# Georgia Klein
# 2019-11-6

# A minesweeper game to play in terminal.

import random
import copy
from colorama import init 
from termcolor import colored 

class Minesweeper:
	
	def __init__(self):
		
		init()
		self.__spots_cleared = 0
		self.__game_won = False
		self.__game_lost = False
		
		# This field contains what is presented to the player.
		self.__guessing_field = []
		# This field contains the location of the mines.
		self.__field = []
		self.create_field()
		# This field contains the final result, showing all of the numbers and mines.
		self.__numbers_field = self.convert_to_numbers(copy.deepcopy(self.__field))
		
		# Begin the game.
		self.print_instructions()
		self.play_round()
	
	def print_instructions(self):
		
		'''Prints a welcome and the instructions for the minesweeper game.'''
		
		print(chr(27) + "[2J")
		print("Welcome to Minesweeper!\n")
		print("The goal of this game is to hit every spot on the field, except for the 10 mines. The mines are randomly placed on the field.")
		print("You will be prompted to choose a spot on the field to hit by entering the value for the row and column of that spot.")
		print("Each spot of the field will have either nothing or a number on it. The number tells you how many adjacent spots contain a mine.")
		input("\nPress enter to continue...")
	
	def create_field(self):
		
		'''Builds an field of all 'H' and a field which includes the mine locations.'''
		
		# Sets up self.__guessing_field to be a field of 'H'.
		for i in range(10):
			self.__field.append([])
			self.__guessing_field.append([])
			for j in range(10):
				self.__field[i].append(0)
				self.__guessing_field[i].append('H')
		
		# Sets up self.__field to have all of the mine locations.	
		done = False
		count = 0
		while done == False:
			# Randomly selects a spot in the field.
			n = random.randrange(10)
			m = random.randrange(10)
			# If there is not already a mine there, it places one there.
			if self.__field[n][m] != '*':
				self.__field[n][m] = '*'
				count += 1
				
			# When 10 mines have been placed the while loop ends.
			if count == 10:
				done = True
	
	def convert_to_numbers(self, field):
		
		# Goes through every single spot in the field.
		for i in range(10):
			for j in range(10):
				# For each spot that is not a mine, the value in the field is
				# set to the number of adjacent spots that have a mine in the.
				if field[i][j] == '*':
					# Left and up
					if (i - 1 >= 0) and (j - 1 >= 0) and field[i-1][j-1] != "*":
						field[i-1][j-1] += 1
					# Up
					if i - 1 >= 0 and field[i-1][j] != "*":
						field[i-1][j] += 1
					# Right and Up
					if (i - 1 >= 0) and (j + 1 < 10) and field[i-1][j+1] != "*":
						field[i-1][j+1] += 1
					# Left
					if j - 1 >= 0 and field[i][j-1] != "*":
						field[i][j-1] += 1
					# Right
					if j + 1 < 10 and field[i][j+1] != "*":
						field[i][j+1] += 1
					# Left and Down
					if (i + 1 < 10) and (j - 1 >= 0) and field[i+1][j-1] != "*":
						field[i+1][j-1] += 1
					# Down
					if (i + 1 < 10) and field[i+1][j] != "*":
						field[i+1][j] += 1
					# Right and Down
					if (i + 1 < 10) and (j + 1 < 10) and field[i+1][j+1] != "*":
						field[i+1][j+1] += 1
						
		return field
	
	def play_round(self):
		
		'''Runs each round, getting the input and running the guessing.'''
		
		# Resets the screen and prints the field.
		print(chr(27) + "[2J")
		self.print_field()
		
		# Gets the users guess.
		row = input("Input row value: ")
		while row.isdigit() == False:
			row = input("Invalid input, please enter the x value again: ")
		column = input("Input column value: ")
		while column.isdigit() == False:
			column = input("Invalid input, please enter the y value again: ")
		row = int(row)
		column = int(column)
		
		self.calculate_guess(column, row)
		
		# Deals with if the the game is over (won or lost), and playing another round.
		if self.__game_lost:
			print(chr(27) + "[2J")
			print("Game over... You hit a mine!")
			self.override_print_field(self.__numbers_field)
		elif self.__game_won:
			print(chr(27) + "[2J")
			print("Congrats, you won!")
			self.override_print_field(self.__numbers_field)
		else:
			self.play_round()
	
	def calculate_guess(self, x, y):
		
		'''Checks to see if the program should begin a recursive check.'''
		
		# If the spot has not been uncovered already and is not a mine, then the
		# recursive_check method is run.
		if self.__guessing_field[x][y] != "H":
			print("That location has already been uncovered, please guess again.\n")
		if self.__numbers_field[x][y] == '*':
			self.__game_lost = True
		else:
			self.__guessing_field[x][y] = self.__numbers_field[x][y]
			self.__spots_cleared += 1
			self.recursively_check(x, y)
		
		# If 90 out of 100 spots have been cleared, that means that the only spots
		# which haven't been cleared are the mines. Thus, it means the user has
		# won the game.
		if self.__spots_cleared == 90:
			self.__game_won = True
	
	def recursively_check(self, x, y):
		
		'''Recursively changes the necessary values in the guessing_field to the values in the number_field.'''
		
		# If the current spot is a '0' in the numbers_field, it means that the spots adjacent it
		# to it need to be uncovered.
		# This will check each spot adjacent to the current spot and do this:
			# If it has not already been uncovered it will be uncovered and self.__spots_cleared will be incremented by 1.
			# This method will be run on the spot in order to check all of the spots adjacent to it. (recursion!)
		if self.__numbers_field[x][y] == 0:
			# Left and Up
			if (x - 1 >= 0) and (y - 1 >= 0) and self.__guessing_field[x-1][y-1] == 'H':
				if self.__guessing_field[x-1][y-1] != self.__numbers_field[x-1][y-1]:
					self.__guessing_field[x-1][y-1] = self.__numbers_field[x-1][y-1]
					self.__spots_cleared += 1
				self.recursively_check(x - 1, y - 1)
			# Up
			if x - 1 >= 0 and self.__guessing_field[x-1][y] == 'H':
				if self.__guessing_field[x-1][y] != self.__numbers_field[x-1][y]:
					self.__guessing_field[x-1][y] = self.__numbers_field[x-1][y]
					self.__spots_cleared += 1
				self.recursively_check(x - 1, y)
			# Right and Up
			if (x - 1 >= 0) and (y + 1 < 10) and self.__guessing_field[x-1][y+1] == 'H':
				if self.__guessing_field[x-1][y+1] != self.__numbers_field[x-1][y+1]:
					self.__guessing_field[x-1][y+1] = self.__numbers_field[x-1][y+1]
					self.__spots_cleared += 1
				self.recursively_check(x - 1, y + 1)
			# Left
			if y - 1 >= 0 and self.__guessing_field[x][y-1] == 'H':
				if self.__guessing_field[x][y-1] != self.__numbers_field[x][y-1]:
					self.__guessing_field[x][y-1] = self.__numbers_field[x][y-1]
					self.__spots_cleared += 1
				self.recursively_check(x, y - 1)
			# Right
			if y + 1 < 10 and self.__guessing_field[x][y+1] == 'H':
				if self.__guessing_field[x][y+1] != self.__numbers_field[x][y+1]:
					self.__guessing_field[x][y+1] = self.__numbers_field[x][y+1]
					self.__spots_cleared += 1
				self.recursively_check(x, y + 1)
			# Left and Down
			if (x + 1 < 10) and (y - 1 >= 0) and self.__guessing_field[x+1][y-1] == 'H':
				if self.__guessing_field[x+1][y-1] != self.__numbers_field[x+1][y-1]:
					self.__guessing_field[x+1][y-1] = self.__numbers_field[x+1][y-1]
					self.__spots_cleared += 1
				self.recursively_check(x + 1, y - 1)
			# Down
			if (x + 1 < 10) and self.__guessing_field[x+1][y] == 'H':
				if self.__guessing_field[x+1][y] != self.__numbers_field[x+1][y]:
					self.__guessing_field[x+1][y] = self.__numbers_field[x+1][y]
					self.__spots_cleared += 1
				self.recursively_check(x + 1, y)
			# Right and Down
			if (x + 1 < 10) and (y + 1 < 10) and self.__guessing_field[x+1][y+1] == 'H':
				if self.__guessing_field[x+1][y+1] != self.__numbers_field[x+1][y+1]:
					self.__guessing_field[x+1][y+1] = self.__numbers_field[x+1][y+1]
					self.__spots_cleared += 1
				self.recursively_check( x + 1, y + 1)	
	
	def print_field(self):
		
		'''Prints out the field that is presented to the player.'''
		
		print(end='  ')
		for n in range(10):
			print(colored(n, 'white'), end=' ')
		print()
		
		m = 0
		for i in self.__guessing_field:
			print(colored(m, 'white'), end=' ')
			m += 1
			for j in i:
				if j == 1:
					print(colored(j, 'cyan'), end=' ')
				elif j == 2:
					print(colored(j, 'green'), end=' ')
				elif j == 3:
					print(colored(j, 'red'), end=' ')
				elif j == 4:
					print(colored(j, 'magenta'), end=' ')
				elif j == '*' or j == 'H':
					print(colored(j, 'grey'), end=' ')
				else:
					print(j, end=' ')
			print()

	def override_print_field(self, field):
		
		'''Prints out any 10 by 10 field that is inputted.'''
		
		print(end='  ')
		for x_value in range(10):
			print(colored(x_value, 'white'), end=' ')
		print()
		
		y_value = 0
		for i in field:
			print(colored(y_value, 'white'), end=' ')
			y_value += 1
			for j in i:
				if j == 1:
					print(colored(j, 'cyan'), end=' ')
				elif j == 2:
					print(colored(j, 'green'), end=' ')
				elif j == 3:
					print(colored(j, 'red'), end=' ')
				elif j == 4:
					print(colored(j, 'magenta'), end=' ')
				elif j == '*' or j == 'H':
					print(colored(j, 'grey'), end=' ')
				else:
					print(j, end=' ')
			print()

def main():
	
	game = Minesweeper()
	
	print("\nThanks for playing!")
	
main()