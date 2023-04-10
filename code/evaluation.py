"""
Evaluation functions
"""


def dummy_evaluation_func(state):
    return 0.0


def distance_evaluation_func(state):
    player = state.get_current_player()
    info = state.get_info()
    score = 0.0
    for p, info_p in info.items():
        if p == player:
            score -= info_p["max_distance"]
        else:
            score += info_p["max_distance"]
    return score


def detailed_evaluation_func(state):
    # TODO
    player = state.get_current_player()
    info = state.get_info()
    score = 0.0
    for p, info_p in info.items():
        #print(p, info_p)
        if p == player:
            score -= info_p["max_distance"] * 0.005
            if info_p["live_four"] > 1:
                score += 1 * 0.15
            else:
                score += info_p["live_four"] * 0.2

            if info_p["live_three"] > 2:
                score += 2 * 0.05
            else:
                score += info_p["live_three"] * 0.05

            if info_p["live_two"] > 3:
                score += 3 * 0.015
            else:
                score += info_p["live_two"] * 0.015
            
            if info_p["four"] >= 1 and info_p["live_three"] >= 0:
                score += 0.075

            score += info_p["four"] * 0.075
            score += info_p["three"] * 0.0125

        else:
            score += info_p["max_distance"] * 0.005
            score -= info_p["live_four"] * 0.8
            score -= info_p["live_three"] * 0.3
            score -= info_p["live_two"] * 0.1
            score -= info_p["four"] * 0.3
            score -= info_p["three"] * 0.1
            if info_p["four"] >= 1 and info_p["live_three"] >= 0:
                score -= 0.1
    #print(score)
    '''本程序在depth=1时极度痴迷于为自己创造live3以至于疯狂的在对手或自己快要赢棋的时候
仍然还在不停的创造live3，但是在depth=2时，这个问题得到极大的缓解，变聪明了很多。
通过使用if-else，减轻这样一种情况，即：两个活三、一个活四为最大计入数量。
'''
    return score
    # ENDDO
    pass


def get_evaluation_func(func_name):
    if func_name == "dummy_evaluation_func":
        return dummy_evaluation_func
    elif func_name == "distance_evaluation_func":
        return distance_evaluation_func
    elif func_name == "detailed_evaluation_func":
        return detailed_evaluation_func
    else:
        raise KeyError(func_name)
