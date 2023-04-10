import random

import copy
import numpy as np
from game import State, Player

from copy import deepcopy


class TreeNode(object):
    """A node in the MCTS tree. Each node keeps track of its total utility U, and its visit-count n_visit.
    """

    def __init__(self, parent, state: State):
        """
        Parameters:
            parent (TreeNode | None): the parent node of the new node.
            state (State): the state corresponding to the new node.
        """
        self.parent = parent
        self.actions = deepcopy(state.get_all_actions())  # a list of all actions
        self.children = {}  # a map from action to TreeNode
        self.n_visits = 0
        self.U = 0  # total utility

    def expand(self, action, next_state):
        """
        Expand tree by creating a new child.

        Parameters:
            action: the action taken to achieve the child.
            next_state: the state corresponding to the child.
        """
        # TODO

        self.children[action] = TreeNode(self, next_state)


        pass

    def get_ucb(self, c):
        """Calculate and return the ucb value for this node in the parent's perspective.
        It is a combination of leaf evaluations U/N and the ``uncertainty'' from the number
        of visits of this node and its parent.
        Note that U/N is in this node's perspective, so a negation is required.

        Parameters:
            c: the trade-off hyperparameter.
        """
        # TODO
        if self.n_visits == 0:
            return 100000

        exploitation = -self.U / self.n_visits
        #there is a -, because we need to get the value from the parent's perspective(the parent is the opponent)
        exploration = c * np.sqrt(np.log(self.parent.n_visits) / self.n_visits)
        return exploitation + exploration


        pass

    def select(self, c):
        """Select action among children that gives maximum UCB value.

        Parameters:
            c: the hyperparameter in the UCB value.

        Return: A tuple of (action, next_node)
        """
        # TODO
        action = None
        next_node = None
        max_value = -100000
        for a in self.actions:
            if a not in self.children:
                continue
            value = self.children[a].get_ucb(c)
            if value > max_value:
                max_value = value
                action = a
                next_node = self.children[a]
        return action, next_node

        pass

    def update(self, leaf_value):
        """
        Update node values from leaf evaluation.

        Parameters:
            leaf_value: the value of subtree evaluation from the current player's perspective.
        """
        # TODO
        self.n_visits += 1
        self.U += leaf_value

        pass

    def update_recursive(self, leaf_value):
        """Like a call to update(), but applied recursively for all ancestors.
        """
        # If it is not root, this node's parent should be updated first.
        if self.parent:
            self.parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def get_unexpanded_actions(self):
        return list(set(self.actions) - set(self.children.keys()))


class MCTS(object):
    """A simple implementation of Monte Carlo Tree Search."""

    def __init__(self, start_state: State, c=5, n_playout=10000):
        """
        Parameters:
            c: the hyperparameter in the UCB value.
            n_playout: the number of total playouts.
        """
        self.start_state = start_state
        self.root = TreeNode(None, start_state)
        self.c = c
        self.n_playout = n_playout

    def playout(self, state: State):
        """
        Run a single playout from the root to the leaf, getting a value at
        the leaf and propagating it back through its parents.
        State is modified in-place, so a copy must be provided.
        """
        node = self.root
        while not state.game_end()[0]:
            unexpanded_actions = node.get_unexpanded_actions()
            if len(unexpanded_actions) > 0:
                action = random.choice(unexpanded_actions)
                state.perform_action(action)
                node.expand(action, state)
                node = node.children[action]
                break
            else:
                # Greedily select next move.
                action, node = node.select(self.c)
                state.perform_action(action)

        leaf_value = self.get_leaf_value(state)
        # Update value and visit count of nodes in this traversal.
        node.update_recursive(leaf_value)

    def get_leaf_value(self, state: State):
        """
        Randomly playout until the end of the game, returning +1 if the current
        player wins, -1 if the opponent wins, and 0 if it is a tie.

        Note: the value should be under the perspective of state.get_current_player()
        """
        # TODO
        #we need to know that only self.n_playout times

        playerme = state.get_current_player()
        while not state.game_end()[0]:
            action = random.choice(state.get_all_actions())
            state.perform_action(action)
        if state.game_end()[0]:
            if state.game_end()[1] == playerme:
                return 1
            elif state.game_end()[1] == -1:
                return 0
            else:
                return -1
        pass
       


class MCTSPlayer(Player):
    """AI player based on MCTS"""
    def __init__(self, c=5, n_playout=2000):
        super().__init__()
        self.c_puct = c
        self.n_playout = n_playout

    def get_action(self, state: State):
        mcts = MCTS(state, self.c_puct, self.n_playout)
        for n in range(self.n_playout):
            state_copy = copy.deepcopy(state)
            mcts.playout(state_copy)
        return max(mcts.root.children.items(),
                   key=lambda act_node: act_node[1].n_visits)[0]
