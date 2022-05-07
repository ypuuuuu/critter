import argparse
import os
import inspect
import importlib
import sys
import threading
import critter_sim
import critter_gui
import critter


def handle_input():
  parser = argparse.ArgumentParser(description="Runs the Critter simulation.")
  
  parser.add_argument('--no-gui', action="store_true", help="run simulation without the GUI and print results directly to the console.")
  parser.add_argument('--width', default=38, type=int, metavar='', help="width of the game board.")
  parser.add_argument('--height', default=35, type=int, metavar='', help="height of the game board.")
  parser.add_argument('--iters', default=1000, type=int, metavar='', help="number of simulation iterations to perform (only used in no-gui mode).")
  parser.add_argument('-n', '--ncritters', default=25, type=int, metavar='', help="number of each critter to add to the simulation.")

  group = parser.add_mutually_exclusive_group()
  group.add_argument('-i', '--include', action='append', type=str, metavar='', help="if specified, the simulation is run only for the provided critters. Critters should be specified by their class name. This flag only accepts one class name; however, you can use the flag multiple times to include different critters. Cannot be used with the --exclude argument.")
  group.add_argument('-e', '--exclude', action='append', type=str, metavar='', help="if specified, the simulation is run for all available critters except those provided. Critters should be specified by their class name. This flag only accepts one class name; however, you can use the flag multiple times to exclude different critters. Cannot be used with the --include argument.")

  args = parser.parse_args()

  return args
  

def import_critters(root='.'):
  """
  Finds all critter definitions in the given directory and returns them as a list of class objects. Only subclasses of Critter will be included.
  """
  classes = []

  # check each python file in directory
  for file in os.listdir(root):
    if file.lower().endswith('.py'):
      # load module
      module_name = inspect.getmodulename(os.path.join(root,file))
      module = importlib.import_module(module_name)

      # check if module contains a Critter subclass 
      for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, critter.Critter):
          if name != "Critter":
            classes.append(obj)

  return classes

def get_critter(name, critters):
	"""
  Returns the requested Critter subclass if it exists in the critters list or None if it does not exist.
  """
	for critter in critters:
		if critter.__name__ == name:
			return critter
	return None


def headless(sim, iterations=1000):
	"""
  Runs the Critter simulation without showing a GUI and prints the results at the end.
  """
	for i in range(iterations):
		sim.update()
	print(sim)


def main():
  # parse input flags and arguments
  args = handle_input()

  # load all Critter subclasses and store them in a list
  critters = import_critters()

  # collect contenders
  
  if args.exclude:
    contenders = critters
    for critter_name in args.exclude:
      contender = get_critter(critter_name, critters)
      if contender != None:
        contenders.remove(contender)
      else:
        print("Error: critter with class name '%s' was not found." % critter_name)
        sys.exit(-1)
  elif args.include:
    contenders = []
    for critter_name in args.include:
      contender = get_critter(critter_name, critters)
      if contender != None:
        contenders.append(contender)
      else:
        print("Error: critter with class name '%s' was not found." % critter_name)
        sys.exit(-1)
  else:
    contenders = critters

  # build simulation and add critter contenders
  sim = critter_sim.CritterSim(args.width, args.height, threading.Lock())
  for critter in contenders:
    sim.add(critter, args.ncritters)

  # show simulation
  if args.no_gui:
    headless(sim, args.iters)
  else:
    c = critter_gui.CritterGUI(sim)
    input()


if __name__ == '__main__':
	main()
