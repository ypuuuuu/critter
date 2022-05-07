import tkinter as tk
import constants

EMPTY_CHAR = '.'


class CritterGUI():
  def __init__(self, sim):
    # Keep track of whether the simulation is currently running or not.
    self.is_running = False

    self.sim = sim
    self.width = 15 * self.sim.width
    self.height = 15 * self.sim.height

    self.root = tk.Tk()
    self.root.grid()
    self.root.title("Critter Lab")

    self.canvas = tk.Canvas(self.root,
                            bg="white",
                            width=self.width,
                            height=self.height)
    self.canvas.grid(columnspan=25, rowspan=10, sticky='W')
    self.rectangle = self.canvas.create_rectangle(
        (0, 0, self.width, self.height), fill='white', outline='white')

    # Class states.
    self.classes_label = tk.Label(self.root,
                                  text='Critter: Alive + Wins = Total')
    self.classes_label.grid(column=25, row=0, columnspan=3)
    self.critter_classes = list(self.sim.critter_class_stats.keys())
    self.num_classes = len(self.critter_classes)
    self.class_state_labels = {}
    ROW = 1
    for x in range(self.num_classes):
      alive = self.sim.critter_class_stats[self.critter_classes[x]].alive
      kills = self.sim.critter_class_stats[self.critter_classes[x]].kills
      total = alive + kills
      self.class_state_labels.update({
          self.critter_classes[x].__name__:
          tk.Label(self.root,
                    text=self.critter_classes[x].__name__ + ": " + str(alive) +
          " + " + str(kills) + " = " + str(total))})
      self.class_state_labels[self.critter_classes[x].__name__].grid(
          column=25, row=ROW)
      ROW = ROW + 1

    self.speed_label = tk.Label(self.root, text='Speed:')
    self.speed_label.grid(column=0, row=10)

    # Change speed of the simulation.
    self.speed_var = tk.IntVar()
    self.speed_var.set(10)
    self.scale = tk.Scale(self.root,
                          variable=self.speed_var,
                          orient='horizontal',
                          length=100,
                          sliderlength=10,
                          from_=1,
                          to=10)
    self.scale.grid(column=1, row=10)

    # Move count.
    self.move_count = 0
    self.move_count_label = tk.Label(self.root, text='0 iterations')
    self.move_count_label.grid(column=3, row=10)

    # Go - when go, start simulation
    self.go_button = tk.Button(self.root,
                                text='Go',
                                bg='green',
                                width=6,
                                command=self.go)
    self.go_button.grid(column=8, row=10)

    # Pause - when pressed, command should pause the simulation
    self.pause_button = tk.Button(self.root,
                                  text='Pause',
                                  bg='red',
                                  width=6,
                                  command=self.pause)
    self.pause_button.grid(column=9, row=10)

    # Step - simulation should still not be running, but should update by 1 move
    self.step_button = tk.Button(self.root,
                                  text='Step',
                                  bg='yellow',
                                  width=6,
                                  command=self.step)
    self.step_button.grid(column=10, row=10)

    # Reset - stop running, display a new critter sim.
    self.reset_button = tk.Button(self.root,
                                  text='Reset',
                                  bg='blue',
                                  width=6,
                                  command=self.reset)
    self.reset_button.grid(column=11, row=10)

    # Representation of the critter world.
    self.chars = [[
        self.canvas.create_text((x * 15 + 7.5, y * 15 + 7.5),
                                text='',
                                font=('Courier New', -15))
        for y in range(self.sim.height)
    ] for x in range(self.sim.width)]

    # Display current critter sim.
    self.display()

  def draw_char(self, char, color, x, y):
    """Displays a single char at position (x, y) on the canvas."""
    self.canvas.itemconfig(self.chars[x][y],
                            text=char,
                            fill=color_to_hex(color),
                            font='Courier 13 bold')
    self.canvas.tag_raise(self.chars[x][y])

  def display(self):
    """Draw all characters representing critters or empty spots."""
    # Clear screen
    self.canvas.tag_raise(self.rectangle)
    # Draw all critters
    for x in range(self.sim.width):
      for y in range(self.sim.height):
        critter = self.sim.grid[x][y]
        if critter:
          self.draw_char(critter.get_char(), critter.get_color(), x, y)
        else:
          self.draw_char(EMPTY_CHAR, constants.BLACK, x, y)

  def update(self):
    """
    Repeatedly updates the GUI with the appropriate characters and colors from the critter simulation, until pause button is pressed to pause simulation. 
    """
    if self.is_running == True:
      self.sim.update()
      self.display()
      self.increment_move()
      self.update_class_stats()
      self.root.after(int(500 / self.speed_var.get()), self.update)

  def increment_move(self):
    """Increment move count by one and display."""
    self.move_count = self.move_count + 1
    self.move_count_label.config(text=str(self.move_count) + ' iterations')

  def update_class_stats(self):
    """Change the display of states of all critter classes."""
    for x in range(self.num_classes):
      alive = self.sim.critter_class_stats[self.critter_classes[x]].alive
      kills = self.sim.critter_class_stats[self.critter_classes[x]].kills
      total = alive + kills
      self.class_state_labels[self.critter_classes[x].__name__].config(
          text=self.critter_classes[x].__name__ + ": " + str(alive) +
          " + " + str(kills) + " = " + str(total))

  def go(self):
    """Actually runs the GUI. Pretty straightforward."""
    self.is_running = True
    self.update()

  def pause(self):
    """Pause updating."""
    self.is_running = False

  def step(self):
    """Move all critters by 1 step."""
    self.is_running = False
    self.sim.update()
    self.display()
    self.increment_move()
    self.update_class_stats()

  def reset(self):
    """Stop simulation, reset critter sim."""
    self.is_running = False
    self.sim.reset()
    self.display()
    self.move_count = 0
    self.move_count_label.config(text='0 iterations')

  def start(self):
    self.root.mainloop()


def color_to_hex(color):
	"""
  Converts RGB colors to hex string, because tkinter thought that passing numeric types as strings was an AWESOME idea.
  """
	return '#%02x%02x%02x'.upper() % (color.r, color.g, color.b)
