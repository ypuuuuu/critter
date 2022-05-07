import constants
import collections
import random

# Just an (x, y) pair, but more readable.
Point = collections.namedtuple('Point', ['x', 'y'])

class CritterSim():
  """
  The main Critter simulation. Takes care of all the logic of Critter fights.
  """
  def __init__(self, width, height, list_lock):
    self.width = width
    self.height = height
    self.critters = []
    self.move_count = 0
    self.num_critters = 0

    # a map of critters to (x, y) positions.
    self.critter_positions = {}

    # a map of critter classes to the number alive of that class.
    self.critter_class_stats = {}
    self.grid = [[None for x in range(height)] for y in range(width)]

    # make sure nothing bad happens due to concurrent list access.
    self.list_lock = list_lock


  def add(self, critter, num):
    """
    Adds a particular critter type num times. The critter should be a class, not an instantiated critter.
    """
    # initialize stats
    if critter not in self.critter_class_stats:
      self.critter_class_stats[critter] = ClassStats(initial_count=num)
    else:
      self.critter_class_stats[critter].count += num
    self.critter_class_stats[critter].alive += num
    self.num_critters = num

    # initialize each critter
    for i in range(num):
      args = CritterSim.create_parameters(critter)
      c = critter(*args)
      self.critters.append(c)
      pos = self.random_location()
      self.critter_positions[c] = pos
      self.grid[pos.x][pos.y] = c


  def create_parameters(critter):
    """
    Returns the appropriate parameters for critters with non-default constructors. Parameterss are returned as a tuple, which will be passed as *args to the critter's constructor.
    """
    if critter.__name__ == 'Mouse':
      return (constants.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),)
    elif critter.__name__ == 'Elephant':
      return (random.randint(1, 15),)
    elif critter.__name__ == 'OppositeElephant':
      return (random.randint(1, 15),)
    else:
      return ()


  def random_location(self):
    """
    Calculate a random location for a Critter to be placed. This is not guaranteed to terminate by any means, but practically we (probably) don't need to be concerned. Returns a 2-tuple of integers.
    """
    x = random.randint(0, self.width - 1)
    y = random.randint(0, self.height - 1)

    while self.grid[x][y] is not None:
      x = random.randint(0, self.width - 1)
      y = random.randint(0, self.height - 1)
      
    return Point(x, y)


  def update(self):
    """
    Takes care of updating all Critters. For each Critter, it firsts moves. If the position it moves to is occupied, the two critters fight, and the loser is destroyed while the winner moves into the position.
    """
    self.move_count += 1
    random.shuffle(self.critters)

    # unclean while loop because we'll be removing any losing critters as we iterate through the list.
    i = 0
    l = len(self.critters)
    while i < l:
      critter1 = self.critters[i]

      # call critter's get_move() method
      critter_info = CritterInfo(self, critter1)
      direction = critter1.get_move(critter_info)

      # move the critter
      CritterSim.verify_move(direction)
      old_position = self.critter_positions[critter1]
      position = self.move(direction, old_position)

      # fight, if necessary
      winner = critter1
      critter2 = self.grid[position.x][position.y]
      if critter2 and position != old_position and critter1 != critter2:
        # fight
        winner = self.fight(critter1, critter2)
        loser = critter1 if winner == critter2 else critter2
        self.critter_positions[winner] = position

        # get rid of the loser
        with self.list_lock:
          index = self.critters.index(loser)
          if index <= i:
            i -= 1
          self.critter_positions.pop(loser)
          self.critters.remove(loser)
          l -= 1

          # make sure we've got an accurate kill/alive count
          self.critter_class_stats[loser.__class__].alive -= 1
          self.critter_class_stats[winner.__class__].kills += 1

      # update positions
      self.grid[old_position.x][old_position.y] = None
      self.grid[position.x][position.y] = winner
      self.critter_positions[winner] = position
      i += 1


  def verify_move(move):
    """Make sure move is valid."""
    if move not in constants.VALID_MOVES:
      raise LocationException("Error: %s is not a valid direction. Critter's must move NORTH, EAST, SOUTH, WEST, or CENTER.." % move)


  def move(self, direction, pos):
    """
    Returns the new position after moving in direction. This assumes that (0, 0) is the top-left.
    """
    if direction == constants.NORTH:
      return Point(pos.x, (pos.y - 1) % self.height)
    elif direction == constants.SOUTH:
      return Point(pos.x, (pos.y + 1) % self.height)
    elif direction == constants.EAST:
      return Point((pos.x + 1) % self.width, pos.y)
    elif direction == constants.WEST:
      return Point((pos.x - 1) % self.width, pos.y)
    elif direction == constants.NORTHEAST:
      return Point((pos.x + 1) % self.width, (pos.y - 1) % self.height)
    elif direction == constants.NORTHWEST:
      return Point((pos.x - 1) % self.width, (pos.y - 1) % self.height)
    elif direction == constants.SOUTHEAST:
      return Point((pos.x + 1) % self.width, (pos.y + 1) % self.height)
    elif direction == constants.SOUTHWEST:
      return Point((pos.x - 1) % self.width, (pos.y + 1) % self.height)
    else:
      return pos


  def fight(self, critter1, critter2):
    """
    Force poor innocent Critters to fight to the death for the entertainment of Oberlin students. Returns the glorious victor.
    """
    # call critter's fight() method
    critter2_info = CritterInfo(self, critter2)
    attack1 = critter1.fight(critter2_info)
    self.verify_attack(attack1)

    critter1_info = CritterInfo(self, critter1)
    attack2 = critter2.fight(critter1_info)
    self.verify_attack(attack2)

    # determine winner and call critter's recover() method
    if (attack1 == constants.ROAR and attack2 == constants.SCRATCH
        or attack1 == constants.SCRATCH and attack2 == constants.POUNCE
        or attack1 == constants.POUNCE and attack2 == constants.ROAR):
      critter1.recover(True, attack2)
      critter2.recover(False, attack1)
      return critter1
    elif attack1 == attack2:
      if random.random() > .5:
        critter1.recover(True, attack2)
        critter2.recover(False, attack1)
        return critter1
      else:
        critter1.recover(False, attack2)
        critter2.recover(True, attack1)
        return critter2
    else:
      critter1.recover(False, attack2)
      critter2.recover(True, attack1)
      return critter2


  def verify_attack(self, attack):
    """
    Make sure students are using the right attacks. If not, throws an exception.
    """
    if attack not in constants.VALID_ATTACKS:
      raise AttackException("Error: %s is not a valid attack. Critter's can only ROAR, POUNCE, or SCRATCH." % attack)


  def reset(self):
    """
    Resets the model, clearing out the whole board and repopulating it with num_critters of the same Critter types.
    """
    self.grid = [[None for x in range(self.height)] for y in range(self.width)]
    self.critter_positions = {}
    self.critters = []
    self.move_count = 0
    new_stats = {}
    for critter_class in self.critter_class_stats.keys():
      new_stats[critter_class] = ClassStats(initial_count=self.num_critters)
      new_stats[critter_class].alive += self.num_critters
      for i in range(self.num_critters):
        args = CritterSim.create_parameters(critter_class)
        c = critter_class(*args)
        self.critters.append(c)
        pos = self.random_location()
        self.critter_positions[c] = pos
        self.grid[pos.x][pos.y] = c
    self.critter_class_stats = new_stats


  def __str__(self):
    """
    Returns a formatted string of the critters in the simulation, sorted by alive+kills.
    """
    results = sorted(self.critter_class_stats.items(), key=lambda stats: -(stats[1].kills + stats[1].alive))

    header = "-" * 45 + '\n'
    header += "%-20s %5s\t%5s\t%5s\n" % ("Critter", "Wins", "Alive", "Total")
    header += "-" * 45 + '\n'

    return header + '\n'.join(['%-20s %5d\t%5d\t%5d' % (critter.__name__, stats.kills, stats.alive, stats.kills + stats.alive) for critter, stats in results])


class ClassStats():
  """
  This would be a named tuple, but they're immutable and that's somewhat unwieldy for this particular case.
  """
  def __init__(self, kills=0, alive=0, initial_count=0):
    self.kills = kills
    self.alive = alive
    self.count = initial_count

  def __repr__(self):
    return '%s %s %s' % (self.kills, self.alive, self.count)


class CritterInfo():
  """
  Helper class for packaging up and providing access to useful information about a critter.
  """
  def __init__(self, sim_obj, critter_obj):
    self._sim = sim_obj
    self._pos = self._sim.critter_positions[critter_obj]
    self._width = self._sim.width
    self._height = self._sim.height
    self._grid = self._sim.grid.copy()
    self._char = critter_obj.get_char()
    self._color = critter_obj.get_color()

  def get_pos(self):
    return (self._pos.x, self._pos.y)

  def get_dimensions(self):
    return (self._width, self._height)

  def get_char(self):
    return self._char

  def get_color(self):
    return self._color

  def get_neighbor(self, direction):
    self._verify_direction(direction)
    neighbor_pos = self._sim.move(direction, self._pos)
    neighbor = self._grid[neighbor_pos.x][neighbor_pos.y]

    return neighbor.__class__.__name__ if neighbor else '.'

  def _verify_direction(self, direction):
    if direction not in constants.VALID_DIRECTIONS:
      raise LocationException("Error: %s is not a valid direction." % direction)


# These exceptions don't really need fancy names
class AttackException(Exception):
	pass


class LocationException(Exception):
	pass
