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
   wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
  wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
   wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww

"""


def display_welcome():
    """
    Function to display the welcome page and ASCII art
    """
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear the terminal screen
    print("                          Welcome to Battleship!")
    print("     Description: In this game, you will play Battleship against the computer.")
    print("                          Try to sink all the computer's ships to win!")
    print(welcome_art)  # Display the ASCII art


# Display the welcome page
display_welcome()

# Ask the player if they want to start the game
start_game = input("Do you want to start the game? (y/n):\n ").lower()
if start_game != 'y':
    print("Goodbye! Come back to play later.")
    exit()

# Ask the player to enter their username
username = input("Enter your username:\n ")


def place_ship(ship_name, size):
    """
    Function to place a ship on the grid
    """
    orientation = random.choice(['horizontal', 'vertical'])
    row = random.randint(0, ROWS - 1)
    col = random.randint(0, COLS - 1)

    if orientation == 'horizontal':
        if col + size > COLS:
            return False
        for i in range(size):
            if grid[row][col + i] != '~':
                return False
        for i in range(size):
            grid[row][col + i] = ship_name
            ships[ship_name].append((row, col + i))
    else:  # vertical
        if row + size > ROWS:
            return False
        for i in range(size):
            if grid[row + i][col] != '~':
                return False
        for i in range(size):
            grid[row + i][col] = ship_name
            ships[ship_name].append((row + i, col))
    return True



for ship_name, ship_size in SHIP_SIZES.items():
    """
    Initialize the ships and mark ship locations as '~'
    """
    ships[ship_name] = []
    ship_objects.append((ship_name, ship_size))
    while not place_ship(ship_name, ship_size):
        ships[ship_name] = []
        grid = [['~' for _ in range(COLS)] for _ in range(ROWS)]  # Reset the grid


def display_grid():
    """
    Function to display the grid with ships hidden
    """
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear the terminal screen
    print("  0 1 2 3 4 5 6 7 8 9")  # Display column numbers
    for row_idx, row in enumerate(grid):
        display_row = []
        for col_idx, col in enumerate(row):
            if hits_grid[row_idx][col_idx] == 'H':
                display_row.append('X')  # Show 'X' for hits
            elif hits_grid[row_idx][col_idx] == 'O':
                display_row.append('O')  # Show 'O' for misses
            else:
                display_row.append('~')  # Show '~' for unguessed spots
        print(f"{chr(65 + row_idx)} {' '.join(display_row)}")  # Use letters for rows
    print("\n")

global last_message
last_message = ""

hile True:
        try:
            letter = input("Enter the row (A-J): ").upper()
            if letter not in letter_to_row:
                print("Invalid input. Please enter letters between A and J.")
                continue  # Restart the loop to get valid input
            col = int(input("Enter the column (0-9): "))

            if col < 0 or col >= COLS:
                print("Invalid input. Please enter numbers between 0 and 9.")
                continue  # Restart the loop to get valid input

            row = letter_to_row[letter]
        except ValueError:
            print("Invalid input. Please enter valid row and column values.")
            continue  # Restart the loop to get valid input

        if hits_grid[row][col] == 'H' or hits_grid[row][col] == 'M':
            print("You've already tried this cell.")
        elif grid[row][col] == '~':
            hits_grid[row][col] = 'O'
            last_message = "Miss!"
        else:
            ship_name = grid[row][col]
            hits_grid[row][col] = 'H'
            ship_hits = sum(1 for r, c in ships[ship_name] if hits_grid[r][c] == 'H')
            last_message = f"You hit the {ship_name}!"
            if ship_hits == SHIP_SIZES[ship_name]:
                last_message = f"You sunk the {ship_name}!"
        break  # Exit the loop when a valid guess is made

while any(ships[ship].count('X') < ship_objects[idx][1] for idx, ship in enumerate(ships)):
    """
    Main game loop
    """
    display_grid()
    print(last_message)
    make_guess()


# End screen
os.system('clear' if os.name == 'posix' else 'cls')  # Clear the terminal screen
print("Congratulations, you've sunk all the computer's ships!")
print(f"Username: {username}")
print("Game Over!")