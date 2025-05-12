import math

from utils.swf import social_welfare_function
from utils.get_weighted_sum import get_weighted_sum

def is_pass_voting(result, threshold):
    if result >= threshold:
        return 1
    else:
        return 0

def is_pass_veto(result_veto, result_voting, threshold_veto = 6, threshold_voting = 5):
    if result_veto >= threshold_veto and result_voting >= threshold_voting:
        return 1
    else:
        return 0


def get_voting_result(test_data, eval_scores, task_setting, voting_type):

    if task_setting == 'seat_apportionment':

        weights = test_data['seat_weights']
        party_name_seq = [stance['party_name'] for stance in test_data['stances']]
        eval_values = [eval_scores[party_name] for party_name in party_name_seq]
        voting_result = get_weighted_sum(weights, eval_values)

        if voting_type == 'veto_power':
            # Whether it is through a veto party only, whether it is through a veto + simple majority, weighted score
            return is_pass_voting(eval_scores[test_data['veto_party_name']], 5), is_pass_veto(eval_scores[test_data['veto_party_name']], voting_result), voting_result
        else:
             # Whether it is by simple majority, whether it is by strengthened majority, weighted score
            return is_pass_voting(voting_result, 5), is_pass_voting(voting_result, 20/3), voting_result
    elif task_setting == 'rawlsianism':
        return social_welfare_function(eval_scores.values(), math.inf)
    elif task_setting == 'utilitarianism':
        return social_welfare_function(eval_scores.values(), 0)
    else:
        # return average of eval_scores
        return sum(eval_scores.values()) / len(eval_scores)

