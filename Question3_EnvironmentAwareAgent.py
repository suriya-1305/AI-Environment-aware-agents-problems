import random
class environment:
  def __init__(self):
    self.limit = random.randint(10,100)
    self.property = {}
    for pos in range(self.limit):
      self.property[pos] = random.choice(["J","S","W","T"])


  def get_limit(self):
   return self.limit

  def get_property(self,pos):
   return self.property[pos]

class env_aware_agent:
  def __init__(self):
    self.position_sense = 0
    self.sweetcount = 0

  def move(self,env):
    while (self.position_sense!=env.get_limit):
      if env.get_property(self.position_sense) == "J":
        print("Jumping at the Tangy")
        self.position_sense=self.position_sense+1
        self.tell_position()
      elif env.get_property(self.position_sense) == "S":
        self.sweetcount=self.sweetcount+1
        print("eating the Sweet")
        self.position_sense +=1
        self.tell_position()
      elif (env.get_property(self.position_sense) == "T" and self.sweetcount==2):
        print("Tangy eatable is found")
        print("eating the tangy")
        self.position_sense=self.position_sense+1
        self.tell_position()
        self.sweetcount=self.sweetcount-2
      else:
        print("Walking without eating")
        self.position_sense=self.position_sense+1
        self.tell_position()
       

  def tell_position(self):
    print("I am currently at position", self.position_sense)

my_agent = env_aware_agent()
my_env = environment()
print("New env limit is =",my_env.get_limit())
my_agent.move(my_env)
