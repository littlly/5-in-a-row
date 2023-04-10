from typing import Tuple
from copy import deepcopy
from game import State, Player

inf = 10000


class MinimaxSearchPlayer(Player):
    """
    Player based on minimax search.
    """

    def get_action(self, state: State):
        """
        An interface for recursively searching.
        """
        assert state.get_current_player() == self.player

        def minimax_search(s: State) -> Tuple:
            """
            Recursively search values of all succeeding nodes, taking maximum of children
            when current player is the agent (self.player) and minimum for opponent.

            Parameters:
                s: the current state

            Return:
                Tuple(value, action): the node value and the best action (if exists)
            
            Note: before you perform an action, you might need to copy the original state for in-place update.
            """
            end, winner = s.game_end()
            value, action = None, None
            if end:
                if winner == -1:
                    value = 0
                else:
                    value = (1 if winner == self.player else -1)
            else:
                # TODO
                def minvalue(s1):
                    end, winner = s1.game_end()
                    if end:
                        if winner == -1:
                            return 0
                        else:
                            return (1 if winner == self.player else -1)
                    else:
                        value = inf
                        for action in s1.get_all_actions():
                            s2 = deepcopy(s1).perform_action(action)
                            value = min(value, maxvalue(s2))
                        return value
                def maxvalue(s1):
                    end, winner = s1.game_end()
                    if end:
                        if winner == -1:
                            return 0
                        else:
                            return (1 if winner == self.player else -1)
                    else:
                        value = -inf
                        for action in s1.get_all_actions():
                            s2 = deepcopy(s1).perform_action(action)
                            value = max(value, minvalue(s2))
                        return value
                value = -inf
                for action in s.get_all_actions():
                    s2 = deepcopy(s).perform_action(action)
                    value = max(value, minvalue(s2))

                    if value == minvalue(s2):
                        actionfinal = action


                # ENDDO
                pass
            return value, actionfinal

        return minimax_search(state)[1]


class AlphaBetaSearchPlayer(Player):
    """
    Player based on alpha-beta search.
    """

    def get_action(self, state: State):
        """
        An interface for recursively searching.
        """
        assert state.get_current_player() == self.player

        def alpha_beta_search(s: State, alpha, beta):
            """
            Based on minimax search, record current maximum value of the max player (alpha)
            and current minimum value of the min player (beta), use alpha and beta to prune.

            Parameters:
                s: the current state
                alpha: the current maximum value of the max player
                beta: the current minimum value of the min player

            Return:
                Tuple(value, action): the node value and the best action (if exists)
            
            Note: before you perform an action, you might need to copy the original state for in-place update.
            """
            end, winner = s.game_end()
            value, action = None, None
            if end:
                if winner == -1:
                    value = 0
                else:
                    value = (1 if winner == self.player else -1)
            else:
                # TODO
                def minvalue(s1, alpha, beta):
                    end, winner = s1.game_end()
                    if end:
                        if winner == -1:
                            return 0
                        else:
                            return (1 if winner == self.player else -1)
                    else:
                        value = inf
                        for action in s1.get_all_actions():
                            s2 = deepcopy(s1).perform_action(action)
                            value = min(value, maxvalue(s2, alpha, beta))
                            if value <= alpha:
                                return value
                            beta = min(beta, value)
                        return value

                def maxvalue(s1, alpha, beta):
                    end, winner = s1.game_end()
                    if end:
                        if winner == -1:
                            return 0
                        else:
                            return (1 if winner == self.player else -1)
                    else:
                        value = -inf
                        for action in s1.get_all_actions():
                            s2 = deepcopy(s1).perform_action(action)
                            value = max(value, minvalue(s2, alpha, beta))
                            if value >= beta:
                                return value
                            alpha = max(alpha, value)
                        return value
                
                value = -inf
                for action in s.get_all_actions():
                    s2 = deepcopy(s).perform_action(action)
                    value = max(value, minvalue(s2, alpha, beta))
                    if value == minvalue(s2, alpha, beta):
                        actionfinal = action

                    #突然意识到alpha-beta剪枝，最外面一层是没办法进行裁剪的
                    #if value >= beta:
                    #    return value, action
                    #alpha = max(alpha, value)
                    

                # ENDDO
                pass

            return value, actionfinal

        return alpha_beta_search(state, -inf, inf)[1]


class CuttingOffAlphaBetaSearchPlayer(Player):

    def __init__(self, max_depth, evaluation_func=None):
        """
        Player based on cutting off alpha-beta search.
        Parameters:
            max_depth: maximum searching depth. The search will stop when the depth exists max_depth.
            evaluation_func: a function taking a state as input and
                outputs the value in the current player's perspective.
        """
        super().__init__()
        self.max_depth = max_depth
        self.evaluation_func = (lambda s: 0) if evaluation_func is None else evaluation_func

    def evaluation(self, state: State):
        """
        Calculate the evaluation value relative to the agent player (rather than state's current player),
        i.e., take negation if the current player is opponent or do nothing else wise.
        """
        value = self.evaluation_func(state)
        if self.player != state.get_current_player():
            value = -value
        return value

    def get_action(self, state: State):
        """
        An interface for recursively searching.
        """
        assert state.get_current_player() == self.player

        def cutting_off_alpha_beta_search(s: State, d, alpha, beta):
            """
            Search for several depth and use evaluation value as cutting off.

            Parameters:
                s: the current state
                d: the remaining search depth, the search will stop when d=0
                alpha: the current maximum value of the max player
                beta: the current minimum value of the min player

            Return:
                Tuple(value, action): the node value and the best action (if exists)
            
            Note: before you perform an action, you might need to copy the original state for in-place update.
            """
            end, winner = s.game_end()
            value, action = None, None
            if end:
                if winner == -1:
                    value = 0
                else:
                    value = (1 if winner == self.player else -1)
            else:
                # TODO
                def minvalue(s1, d, alpha, beta):
                    end, winner = s1.game_end()
                    if end:
                        if winner == -1:
                            return 0
                        else:
                            return (1 if winner == self.player else -1)
                    elif d == 0:
                        return self.evaluation(s1)
                    else:
                        value = inf
                        for action in s1.get_all_actions():
                            s2 = deepcopy(s1).perform_action(action)
                            value = min(value, maxvalue(s2, d-1, alpha, beta))
                            if value <= alpha:
                                return value
                            beta = min(beta, value)
                        return value
                def maxvalue(s1, d, alpha, beta):
                    end, winner = s1.game_end()
                    if end:
                        if winner == -1:
                            return 0
                        else:
                            return (1 if winner == self.player else -1)
                    elif d == 0:
                        return self.evaluation(s1)
                    else:
                        value = -inf
                        for action in s1.get_all_actions():
                            s2 = deepcopy(s1).perform_action(action)
                            value = max(value, minvalue(s2, d-1, alpha, beta))
                            if value >= beta:
                                return value
                            alpha = max(alpha, value)
                        return value

                value = -inf
                for action in s.get_all_actions():
                    s2 = deepcopy(s).perform_action(action)
                    value = max(value, minvalue(s2, d-1, alpha, beta))
                    if value == minvalue(s2, d-1, alpha, beta):
                        actionfinal = action
                pass
            return value, actionfinal

        return cutting_off_alpha_beta_search(state, self.max_depth, -inf, inf)[1]
