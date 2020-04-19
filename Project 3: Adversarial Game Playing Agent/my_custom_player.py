from sample_players import DataPlayer

class CustomPlayer(DataPlayer):
  def get_action(self, state):
    if self.context is None:
        self.context = {'node': 0, 'layer': 0}

    import random
    if state.ply_count < 2:
      self.queue.put(random.choice(state.actions()))
      
    else:
      depth = 1

      while True:
        node = self.context['node']

        self.queue.put(self.alpha_beta_search(state, depth, self.combined))
        self.context['layer'] += depth

        # terminate if no new nodes are found
        if self.context['node'] - node == depth:
              return
        depth += 1
        
  # given in the lectures
  def alpha_beta_search(self, state, depth, heuristic):
    def min_value(state, depth, alpha, beta):
      self.context['node'] += 1

      if state.terminal_test():
        return state.utility(self.player_id)

      if depth <= 0:
          return heuristic(state)
      
      v = float("inf")
      for a in state.actions():
        v = min(v, max_value(state.result(a), depth-1, alpha, beta))
        if v <= alpha: return v
        beta = min(beta, v)
      return v

    def max_value(state, depth, alpha, beta):
      self.context['node'] += 1

      if state.terminal_test():
        return state.utility(self.player_id)
      
      if depth <= 0: return heuristic(state)

      v = float("-inf")
      for a in state.actions():
        v = max(v, min_value(state.result(a), depth-1, alpha, beta))
        if v >= beta: return v
        alpha = max(alpha, v)
      return v

    self.context['node'] += 1
    
    alpha = float("-inf")
    beta = float("inf")
    
    best_score = float("-inf")
    best_move = state.actions()[0]

    for a in state.actions():
      v = min_value(state.result(a), depth-1, alpha, beta)
      alpha = max(alpha, v)

      if v > best_score:
        best_score = v
        best_move = a
    return best_move

  # baseline function given in project introduction
  def baseline(self, state):
    return len(state.liberties(state.locs[self.player_id])) - \
           len(state.liberties(state.locs[1-self.player_id]))

  # heuristic which takes in account the current locations of
  # each player to the center-most cell
  def central(self, state):
    pos_1 = state.locs[self.player_id]
    pos_2 = state.locs[1-self.player_id]

    x1, y1 = (pos_1%(11+2), pos_1//(9+2))
    x2, y2 = (pos_2%(11+2), pos_2//(9+2))

    # center coordinates: [(11-1)/2, (9-1)/2] = [5, 4]
    return -(x1-5)**2 - (y1-4)**2 + (x2-5)**2 + (y2-4)**2

  # combining both heuristics to create a final heuristic
  def combined(self, state):
    return 0.5*self.baseline(state) + 1.5*self.central(state) 