import constants

class Critter():
  """Defines a generic critter."""

  def __init__(self):
    """Constructor"""
    pass


  def get_color(self):
    """
    Getter for current color.

    Return:
      Your current color.
    """
    pass


  def get_char(self):
    """
    Getter for character.

    Return:
      A character used to represent your critter.
    """
    pass


  def get_move(self, self_info):
    """
    Determines and returns a direction based on movement behavior.

    Params:
      self_info - a CritterInfo object containing information about your critter.

    Return:
      A cardinal direction, in the form of a constant (NORTH, EAST, SOUTH, or WEST).
    """
    pass


  def fight(self, opp_info):
    """
    Determines and returns an attack based on fight behavior.

    Params:
      opp_info - a CritterInfo object containing information about the current opponent.

    Return:
      Your attack, in the form of a constant (ROAR, POUNCE, or SCRATCH).
    """
    pass


  def recover(self, won, opp_attack):
    """
    Actions to be performed after a fight.

    Params:
      won - a Boolean indicate whether the fight was won
      opp_attack - the opponent's attack (ROAR, POUNCE, or SCRATCH)
    """
    pass


  def neighbor_threat(self, self_info, direction):
    '''
    Given a direction, determines the number of critters in the "neighborhood" of that direction and returns the number from [0,3].

    Example:
      neighbor_threat(self_info, constants.NORTH) will return 3 if there are critters NORTH, NORTHEAST, and NORTHWEST of the current critter.

    Params:
      self_info - a CritterInfo object containing information about your critter.
      direction - what direction to search for critters (must be a direction CONSTANT)

    Return:
      The number of critters in given direction as an int between 0 and 3
    '''
    if direction not in constants.MAP_DIRECTIONS.keys():
        raise TypeError('Error: direction passed as argument to self.neighbors must be a constant.py direction.')

    relevant_directions = constants.MAP_DIRECTIONS[direction]
    result = 0
    for d in relevant_directions:
        neighbor_info = self_info.get_neighbor(d)
        if neighbor_info != '.': #baddie
            result += 1
                
    return result


  def __str__(self):
    """Provides class name."""
    return '%s' % (self.__class__.__qualname__)
