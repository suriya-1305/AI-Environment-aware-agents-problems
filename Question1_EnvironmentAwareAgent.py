import random
class environment:
  def __init__(self):
    self.limit = random.randint(10,100)
    self.property = {}
    for pos in range(self.limit):
      self.property[pos] = "J"
    else:
      self.property[pos] = "O"

  def get_limit(self):
   return self.limit

  def get_property(self,pos):
   return self.property[pos]

class env_aware_agent:
  def __init__(self):
    self.position_sense = 0

  def move(self,env):
    while (self.position_sense!=env.get_limit):
      self.tell_position()
      if env.get_property(self.position_sense) == "O":
        print("obstacle is detected")
        self.position_sense=self.position_sense+2
        self.tell_position()
      else:
        print("flat surface is detected")
        self.position_sense=self.position_sense+1
        self.tell_position()
        if (self.position_sense!=env.get_limit):
          print("Reached the destination")

  def tell_position(self):
    print("I am currently at position", self.position_sense)

my_agent = env_aware_agent()
my_env = environment()
print("New env limit is =",my_env.get_limit())
my_agent.move(my_env)
