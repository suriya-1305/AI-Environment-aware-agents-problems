import random
class Solver:
  def __init__(self, search):
    self.search = search;
    self.value_function = [];
    self.initialize_value_function();
    self.is_list_of_list = False;
    
  def initialize_value_function(self):
    list_of_states = self.search.S();
    for individual_list in list_of_states:
      if isinstance(individual_list, int):
        is_list_of_list = False;
      else:
        is_list_of_list = True;
    if is_list_of_list:
      self.is_list_of_list = True;
      for individual_items in list_of_states:
        self.value_function.append(0);
    else:
      self.is_list_of_list = False;
      for individual_items in list_of_states:
        self.value_function.append(0);

  def get_neighbours(self, row, column, possible_actions):
    neighbours_list = [];
    neighbours_actions = [];
    neighbours_list.append((row + 1) + " " + column);
    neighbours_actions.append("down");
    neighbours_list.append((row - 1) + " " + column);
    neighbours_actions.append("up");
    neighbours_list.append(row + " " + (column + 1));
    neighbours_actions.append("right");
    neighbours_list.append(row + " " + (column - 1));
    neighbours_actions.append("left");
    return neighbours_list, neighbours_actions;
    
  def get_neighbours(self, row, possible_actions):
    neighbours_list = [];
    neighbours_actions = [];
    neighbours_list.append((row + 1));
    neighbours_actions.append("right");
    neighbours_list.append((row - 1));
    neighbours_actions.append("left");      
    return neighbours_list, neighbours_actions;
  
  def calculate_value_function_iterative(self):
    possible_actions = self.search.A();
    state_space = self.search.S();
    neighbours_list = [];
    neighbours_actions = [];
    delta_too_small = False;
    iterations = 0;
    temp = 0; 
    while True:
      temp = temp + 1;
      iterations = iterations + 1;
      if self.is_list_of_list == True:
        for individual_list_count in range(0, len(self.value_function)):
          neighbours_list =[];
          neighbours_actions = [];
          value_function_neighbour_states = [];
          value_function_neighbour_states_actions_sum = [];
          for possible_actions_item in possible_actions:
            value_function_neighbour_states = [];
            for state_space_item in state_space:
              value_function_neighbour_states.append(self.calculate_value_function_neighbours(state_space[individual_list_count], state_space_item, possible_actions_item)); 
            value_function_neighbour_states_actions_sum.append(sum(value_function_neighbour_states));
          self.value_function[individual_list_count] = max(value_function_neighbour_states_actions_sum);
          if ((self.value_function[individual_list_count] - delta) != 0 and (self.value_function[individual_list_count] - delta) < 0.01):
            delta_too_small = True;
          if delta_too_small:
            break;
      else:
        for individual_list_count in range(0, len(self.value_function)):
          neighbours_list = [];
          neighbours_actions = [];
          delta = self.value_function[individual_list_count];
          neighbours_list, neighbours_actions = self.get_neighbours(individual_list_count, possible_actions);
          value_function_neighbour_states = [];
          value_function_neighbour_states_actions_sum = [];
          for possible_actions_item in possible_actions:
            value_function_neighbour_states = [];
            for state_space_item in state_space:
              value_function_neighbour_states.append(self.calculate_value_function_neighbours(state_space[individual_list_count], state_space_item, possible_actions_item));
            value_function_neighbour_states_actions_sum.append(sum(value_function_neighbour_states));
          self.value_function[individual_list_count] = max(value_function_neighbour_states_actions_sum);
          if ((self.value_function[individual_list_count] - delta) != 0 and (self.value_function[individual_list_count] - delta) < 0.01):
            delta_too_small = True;
          if delta_too_small:
            break;
        if delta_too_small:
          break;
  
  def calculate_value_function_neighbours(self, current_state, neighbour, action):
    transition_probability = self.search.P(current_state, action, neighbour);
    reward = self.search.R(neighbour);
    discount_factor = self.search.gamma();
    value_function_estimate = transition_probability * (reward + (discount_factor * self.value_function[self.search.S().index(neighbour)]));
    return value_function_estimate;

  def calculate_optimal_policy(self, state):
    list_of_states = self.search.S();
    is_list_of_list = all(isinstance(individual_list, list) for individual_list in list_of_states);
    if is_list_of_list:
      pass;
    else:
      value_func = [];
      value_func_actions = [];
      if (((state + 1) < len(self.value_function)) and ((state + 1) >= 0)):
        value_func.append(self.value_function[(state + 1)]);
        value_func_actions.append("right");
      if (((state - 1) < len(self.value_function)) and ((state - 1) >= 0)):
        value_func.append(self.value_function[(state - 1)]);
        value_func_actions.append("left");
      value_func.append(self.value_function[state]);
      value_func_actions.append("do_nothing");
      policy = max(value_func);
      action = value_func_actions[value_func.index(policy)];
      if action == "do_nothing":
        if state == 0:
          action = "left";
        elif state == (len(self.value_function) - 1):
          action = "right";
      return action;
    
  def solve(self):

    self.calculate_value_function_iterative();
    actions_to_take = [];
    for value_function_item in self.value_function:
      actions_to_take.append(self.calculate_optimal_policy(self.value_function.index(value_function_item)));
    return actions_to_take;



class GoldSearch:
  def __init__(self, wall_locations, pit_locations, goldsearch_location, gold_location, start_location):
    self.actions = ["do nothing", "left", "right", "up", "down", "shoot left", "shoot right", "shoot up", "shoot down"];
    self.arrow_count = 1;
    self.states = [];
    self.define_states_space(wall_locations);
    self.pit_locations = pit_locations;
    self.gold_location = gold_location;
    self.start_location = start_location;
    self.wall_locations = wall_locations;
    self.goldsearch_location = goldsearch_location;

  def define_states_space(self, wall_locations):
    max_number_of_rows = 0;
    max_number_of_columns = 0;
    min_number_of_rows = 0;
    min_number_of_columns = 0;
    if len(wall_locations) > 0:
      min_number_of_rows = wall_locations[0][0];
      min_number_of_columns = wall_locations[0][1];
    for wall_locations_temp in wall_locations:
      if max_number_of_rows < wall_locations_temp[0]:
        max_number_of_rows = wall_locations_temp[0];
      if max_number_of_columns < wall_locations_temp[1]:
        max_number_of_columns = wall_locations_temp[1];
      if min_number_of_rows > wall_locations_temp[0]:
        min_number_of_rows = wall_locations_temp[0];
      if min_number_of_columns > wall_locations_temp[1]:
        min_number_of_columns = wall_locations_temp[1];
    for rows_count in range(min_number_of_rows, (max_number_of_rows + 1)):
      for columns_count in range(min_number_of_columns, (max_number_of_columns + 1)):
        self.states.append((rows_count, columns_count));
  def A(self):
    return self.actions;

  def S(self):
    return self.states;

  def P(self, s, a, u):
    if s == u:
      if a == self.actions[7]:
        if self.goldsearch_location != None:
          if self.goldsearch_location[1] == s[1] and self.goldsearch_location[0] < s[0]:
            self.goldsearch_location = None;
            return 0.9;
      elif a == self.actions[8]:
        if self.goldsearch_location != None:
          if self.goldsearch_location[1] == s[1] and self.goldsearch_location[0] > s[0]:
            self.goldsearch_location = None;
            return 0.9;
      elif a == self.actions[6]:
        if self.goldsearch_location != None:
          if self.goldsearch_location[0] == s[0] and self.goldsearch_location[1] > s[1]:
            self.goldsearch_location = None;
            return 0.9;
      elif a == self.actions[5]:
        if self.goldsearch_location != None:
          if self.goldsearch_location[0] == s[0] and self.goldsearch_location[1] < s[1]:
            self.goldsearch_location = None;
            return 0.9;
      else:
        return 0;
    elif s != u:
      if a == self.actions[1] and u[1] == (s[1] - 1):
        if ((self.goldsearch_location == u) or (u in self.pit_locations)):
          return 0;
        elif self.gold_location == u:
          return 0.9;
        return 0.1;
      if a == self.actions[1] and u[1] == (s[1] + 1):
        if ((self.goldsearch_location == u) or (u in self.pit_locations)):
          return 0;
        elif self.gold_location == u:
          return 0.9;
        return 0;
      if a == self.actions[2] and u[1] == (s[1] + 1):
        if ((self.goldsearch_location == u) or (u in self.pit_locations)):
          return 0;
        elif self.gold_location == u:
          return 0.9;
        return 0.1;
      if a == self.actions[2] and u[1] == (s[1] - 1):
        if ((self.goldsearch_location == u) or (u in self.pit_locations)):
          return 0;
        elif self.gold_location == u:
          return 0.9;
        return 0;
      if a == self.actions[3] and u[0] == (s[0] - 1):
        if ((self.goldsearch_location == u) or (u in self.pit_locations)):
          return 0;
        elif self.gold_location == u:
          return 0.9;
        return 0.1;
      if a == self.actions[3] and u[0] == (s[0] + 1):
        if ((self.goldsearch_location == u) or (u in self.pit_locations)):
          return 0;
        elif self.gold_location == u:
          return 0.9;
        return 0;
      if a == self.actions[4] and u[0] == (s[0] + 1):
        if ((self.goldsearch_location == u) or (u in self.pit_locations)):
          return 0;
        elif self.gold_location == u:
          return 0.9;
        return 0.1;
      if a == self.actions[4] and u[0] == (s[0] - 1):
        if ((self.goldsearch_location == u) or (u in self.pit_locations)):
          return 0;
        elif self.gold_location == u:
          return 0.9;
        return 0;
    return 0;
    
  def R(self, s):
    if ((s in self.pit_locations) or (s == self.goldsearch_location)):
      return -100;
    elif s == self.gold_location:
      return 100;
    else:
      return -1;

  def initial_state(self):
    return self.start_location;

  def gamma(self):
    return 0.99

search = GoldSearch([(0,0),(1,0),(2,0),(3,0),(3,1),(3,2),(3,3),(2,3),(1,3),(0,3),(0,2),(0,1)], [(1,2)], (2,1), (2,2), (1,1));
s = Solver(search)
output = s.solve()
print(output);

