import os
import random

# Constants for grid dimensions
ROWS = 10
COLS = 10

# Constants for ship sizes
SHIP_SIZES = {'Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2}

# Create an empty grid and a grid to track hits, initially marking ship locations as '~'
grid = [['~' for _ in range(COLS)] for _ in range(ROWS)]
hits_grid = [['~' for _ in range(COLS)] for _ in range(ROWS)]

# Create a dictionary to store ship data
ships = {}

# Create a list to store ship objects
ship_objects = []

# Create a mapping of letters to row numbers
letter_to_row = {letter: row for row, letter in enumerate('ABCDEFGHIJ')}

# ASCII art for the welcome page
welcome_art =                   """
                                            # #  ( )
                                        ___#_#___|__
                                    _  |____________|  _
                             _=====| | |            | | |==== _
                        =====| |.------------------------. | |====
   <------------------'   .    .    .    .    .    .   .    . '------------/
     \                                                                    /
      \______________________________________________________SRN_________/
   wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
  wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
   wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww

"""

def display_welcome():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("Welcome to Battleship!")
    print("Description: In this game, you will play Battleship against the computer.")
    print("Try to sink all the computer's ships to win!")
    print(welcome_art)

# Display the welcome page
display_welcome()

# Ask the player if they want to start the game
start_game = input("Do you want to start the game? (y/n): ").lower()
if start_game != 'y':
    print("Goodbye! Come back to play later.")
    exit()

# Ask the player to enter their username
username = input("Enter your username: ")

def place_ship(ship_name, size):
    orientation = random.choice(['horizontal', 'vertical'])
    while True:
        if orientation == 'horizontal':
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLS - size)
        else:  # vertical
            row = random.randint(0, ROWS - size)
            col = random.randint(0, COLS - 1)

        if all(grid[r][c] == '~' for r in range(row, row + (size if orientation == 'horizontal' else 1))
               for c in range(col, col + (size if orientation == 'vertical' else 1))):
            for i in range(size):
                if orientation == 'horizontal':
                    grid[row][col + i] = ship_name
                    ships[ship_name].append((row, col + i))
                else:
                    grid[row + i][col] = ship_name
                    ships[ship_name].append((row + i, col))
            break

for ship_name, ship_size in SHIP_SIZES.items():
    ships[ship_name] = []
    ship_objects.append((ship_name, ship_size))
    while not place_ship(ship_name, ship_size):
        ships[ship_name] = []

def display_grid():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("  0 1 2 3 4 5 6 7 8 9")
    for row_idx, row in enumerate(grid):
        display_row = []
        for col_idx, col in enumerate(row):
            if hits_grid[row_idx][col_idx] == 'H':
                display_row.append('X')
            elif hits_grid[row_idx][col_idx] == 'O':
                display_row.append('O')
            else:
                display_row.append('~')
        print(f"{chr(65 + row_idx)} {' '.join(display_row)}")

def make_guess():
    global last_message
    while True:
        messages = []
        try:
            letter = input("Enter the row (A-J): ").upper()
            if letter not in letter_to_row:
                print("Invalid input. Please enter letters between A and J.")
                continue
            col = int(input("Enter the column (0-9): "))
            if col < 0 or col >= COLS:
                print("Invalid input. Please enter numbers between 0 and 9.")
                continue
            row = letter_to_row[letter]
        except ValueError:
            print("Invalid input. Please enter valid row and column values.")
            continue
        if hits_grid[row][col] == 'H' or hits_grid[row][col] == 'O':
            messages.append("You've already tried this cell.")
        elif grid[row][col] == '~':
            hits_grid[row][col] = 'O'
            messages.append("Miss!")
        else:
            ship_name = grid[row][col]
            hits_grid[row][col] = 'H'
            ship_hits = sum(1 for r, c in ships[ship_name] if hits_grid[r][c] == 'H')
            messages.append(f"You hit the {ship_name}!")
            if ship_hits == SHIP_SIZES[ship_name]:
                messages.append(f"You sunk the {ship_name}!")
        last_message = "\n".join(messages)
        break

def all_ships_sunk():
    for ship_name, ship_size in SHIP_SIZES.items():
        if sum(1 for r, c in ships[ship_name] if hits_grid[r][c] == 'H') < ship_size:
            return False
    return True

while not all_ships_sunk():
    display_grid()
    make_guess()

os.system('clear' if os.name == 'posix' else 'cls')
print("Congratulations, you've sunk all the computer's ships!")
print(f"Username: {username}")
print("Game Over!")
