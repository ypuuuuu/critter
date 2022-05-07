import collections

# Structure for storing colors
Color = collections.namedtuple('Color', ['r', 'g', 'b'])

# Colors
GRAY = Color(128, 128, 128)
BLACK = Color(0, 0, 0)
ORANGE = Color(255, 165, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
PURPLE = Color(186, 85, 211)
BROWN = Color(165, 42, 42)
PINK = Color(255, 192, 203)

# Directions
NORTH = -2
NORTHEAST = 27
NORTHWEST = 102
SOUTH = 4
SOUTHEAST = 99
SOUTHWEST = -31
EAST = 3
WEST = 19
CENTER = 11

VALID_MOVES = (NORTH, EAST, SOUTH, WEST, CENTER)
VALID_DIRECTIONS = (NORTHWEST, NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST)

# Map between the directions and their related "cardinal" directions
MAP_DIRECTIONS = {NORTH : [NORTHWEST, NORTH, NORTHEAST],  EAST: [NORTHEAST, EAST, SOUTHEAST],  SOUTH: [SOUTHEAST, SOUTH, SOUTHWEST], WEST: [SOUTHWEST, WEST, NORTHWEST]}

# Attacks
ROAR = 28
POUNCE = -10
SCRATCH = 55

VALID_ATTACKS = (ROAR, POUNCE, SCRATCH)
