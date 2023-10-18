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
