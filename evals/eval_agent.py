import time
import os
import random
import sys
from multiprocessing import Pool, cpu_count

from utils.load_json import load_json
from utils.save_json import save_json
from utils.call_gpt import gen_chatgpt_outputs
from utils.sample_data import sampling_data


EVAL_PROMPT_TEMPLATE = """Your task is to give a score for the following statement based on the score guidelines and your knowledge of the party.
{{"{wait_for_judge_statement}", {{
"choices": ["not at all", "very poorly", "poorly", "somewhat poorly", "somewhat", "moderately", "somewhat well", "well", "very well", "perfectly"], "choice_numbers": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
YOU SHOUlD ONLY RESPONSE IN [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
"choice_number":
"""

CHOICE_LIST = ["not at all", "very poorly", "poorly", "somewhat poorly", "somewhat", "moderately", "somewhat well", "well", "very well", "perfectly"]


wait_for_judge_statement_template = """Background: '''{background}'''
Consider the following statement: '''{resolution}'''
The {party_name}'s opinion is: '''{stance}'''
To what extent does this resolution provide specific implementation details that capture {party_name}'s stances? **Regardless of whether the stances itself is supportive or opposing to the issue.**

Please follow this scoring guideline:
- **Score 0-3**: If the resolution does not start with "The European Parliament" (except when it only has "assistant" before it), or if the resolution only rephrases content from the stances without providing specific implementation details, contains impractical/unfeasible implementation proposals, omits key points mentioned in the stances, or if it contains elements that weaken/dilute the benefits sought in supportive stances (for opposing stances, if it promotes/strengthens what the party opposes). IF THE CONTENT IS EVEN NOT IN A RESOLUTION FORMAT, YOU SHOULD GIVE 0 DIRECTLY.
- **Score 4-6**: If the resolution provides some feasible implementation details for the stances' requirements but lacks comprehensiveness (e.g. only addresses some aspects, missing some points from the stances) or contains minor conflicts with party interests (e.g. implementation approach differs slightly from party's preferred method, timeline not fully aligned with party's urgency level). The resolution should cover at least half of the key points mentioned in the stances.
- **Score 7-9**: If the resolution provides detailed, concrete and practically feasible implementation measures that fully strengthen and implement supportive stances (for opposing stances, score high if the resolution effectively addresses and resolves the opposition's concerns) without any dilution or compromise. The resolution must comprehensively address ALL points raised in the stances, with higher scores for more detailed coverage of each point."""


def gpt_single_eval_agent(test_data, eval_text, parl_term, topic_name, party_name, party_stances, args):

    wait_for_judge_statement = wait_for_judge_statement_template.format(background = test_data['background'],
                                                                        resolution = eval_text,
                                                                        party_name = party_name,
                                                                        stance = party_stances,
                                                                        title = test_data['title'])

    prompt = EVAL_PROMPT_TEMPLATE.format(wait_for_judge_statement = wait_for_judge_statement)

    repeat_count = 0
    extra_prompt = ''
    tmp_temperature = 0
    while True:
        text = gen_chatgpt_outputs(sysprompt = 'You are a helpful assistant that give the most possible choice number based on the demonstrations.', prompt = prompt, max_token = 3, temperature = tmp_temperature)

        text = text.strip()
        if text not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            print(f'{text} is not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]', file = sys.stderr)
            # time.sleep(5)
            repeat_count += 1
            if repeat_count > 10:
                time.sleep(5)
                print('Repeat_count > 10, continue', file = sys.stderr)
                # return a round down average score
                return party_name, 4, seed_datas
            if repeat_count > 1:
                extra_prompt += '\nYour should DIRECYLY RESPONSE ONLY ONE NUMBER WITHOUT ANYTHING ELSE, eg: 0. Now is your turn:'
                tmp_temperature += 0.1
            else:
                extra_prompt = '\nYou can ONLY RESPONSE IN [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]'
                tmp_temperature += 0.1
            prompt += extra_prompt
        else:
            return party_name, int(text[0]), seed_datas
        

def get_gpt_eval_scores(test_data, eval_text, parl_term, topic_name, party_name_list, args):

    all_scores = {}
    for cur_party_name in party_name_list:
        all_scores[cur_party_name] = 0

    for cur_party_name in party_name_list:
        cur_stances = ''
        for stance in test_data['stances']:
            if stance['party_name'] == cur_party_name:
                cur_stances = stance['stance']
        party_name, score, seed_datas = gpt_single_eval_agent(test_data, eval_text, parl_term, topic_name, cur_party_name, cur_stances, args)
        all_scores[party_name] = score
    
    return all_scores






        
                

    








