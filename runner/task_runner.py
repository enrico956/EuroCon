import time
import os

from tqdm import tqdm

from utils.load_json import load_json
from utils.save_json import save_json
from utils.load_models import load_models
from utils.call_models import gen_model_responses
from utils.call_gpt import gen_chatgpt_outputs
from utils.sample_data import sampling_data
from evals.get_voting_result import get_voting_result
from evals.eval_agent import get_gpt_eval_scores
from config import args as task_args
from runner.task_prompts import (task_system_prompt,
                                 task_prompt_tempalte,
                                 one_example_resolution,
                                 opinion_prompt_template,
                                 task_requirement_templates,
                                 seat_apportionment_weight_template,
                                 voting_requirement_templates)


# start to run tasks
def run_task(data, model, tokenizer):
    # construct opinion prompt
    opinion_prompt = ''
    for stance in data['stances']:
        opinion_prompt += opinion_prompt_template.format(party_name=stance['party_name'], stance=stance['stance']) + '\n'
    
    # construct task requirement prompt
    if task_args.task_setting == 'seat_apportionment':
        # Construct seat apportionment weight prompt
        seat_apportionment_weight_prompt = ''
        for stance, weight in zip(data['stances'], data['seat_weights']):
            seat_apportionment_weight_prompt += seat_apportionment_weight_template.format(party_name=stance['party_name'], seat_proportion=weight * 100) + '\n'

        task_requirement_prompt = task_requirement_templates['seat_apportionment'].format(seat_apportionment_weights=seat_apportionment_weight_prompt)
        
    else:  # in [rawlsianism, utilitarianism]
        task_requirement_prompt = task_requirement_templates[task_args.task_setting]
        
    # construct voting requirement prompt
    if task_args.voting_threshold_setting == 'veto_power':
        voting_requirement_prompt = voting_requirement_templates['veto_power'].format(veto_party_name=data['veto_party_name'])
    else:  # in [simple_majority, 2_3_majority, none]
        voting_requirement_prompt = voting_requirement_templates[task_args.voting_threshold_setting]
    
    if task_args.task_setting == 'seat_apportionment':
        task_requirement_prompt += f"\n{voting_requirement_prompt}"

    # sample example resolution for few shot
    # also can use one_example_resolution for few shot
    few_shot_example_resolution_datas = load_json(f'datas/topic_datas/{task_args.eval_topic}.json')
    example_resolution = sampling_data(few_shot_example_resolution_datas, 1)[0]['resolution']

    # construct task prompt
    task_prompt = task_prompt_tempalte.format(background = data['background'],
                                              party_num = task_args.party_num,
                                              topic = data['title'],
                                              stances = opinion_prompt,
                                              task_requirements = task_requirement_prompt,
                                              resolution = example_resolution)
    
    # get LLM response
    responses = gen_model_responses(model = model, 
                                    tokenizer = tokenizer, 
                                    args = task_args, 
                                    sysprompt = task_system_prompt, 
                                    prompt = task_prompt,)
    
    # get eval scores, the eval_scores is a dict, key is party_name, value is score
    eval_scores = get_gpt_eval_scores(test_data = data,
                                      eval_text = responses,
                                      parl_term = data['parliament_terms'],
                                      topic_name = task_args.eval_topic,
                                      party_name_list = [stance['party_name'] for stance in data['stances']],
                                      args = task_args)
    
    # get voting results
    if task_args.task_setting == 'seat_apportionment':
        if task_args.voting_threshold_setting == 'veto_power':
            is_pass_simple_majority, is_pass_2_3_majority = -1, -1
            is_pass_simple_veto, is_pass_veto, voting_result = get_voting_result(data, eval_scores, task_args.task_setting, task_args.voting_threshold_setting)
        else:
            is_pass_simple_veto, is_pass_veto = -1, -1
            is_pass_simple_majority, is_pass_2_3_majority, voting_result = get_voting_result(data, eval_scores, task_args.task_setting, task_args.voting_threshold_setting)
    else:
        is_pass_simple_veto = is_pass_veto = is_pass_simple_majority = is_pass_2_3_majority = -1
        voting_result = get_voting_result(data, eval_scores, task_args.task_setting, task_args.voting_threshold_setting)

    return {'responses': responses, 
            'eval_scores': eval_scores, 
            'is_pass_simple_veto': is_pass_simple_veto, 
            'is_pass_veto': is_pass_veto, 
            'is_pass_simple_majority': is_pass_simple_majority, 
            'is_pass_2_3_majority': is_pass_2_3_majority, 
            'voting_result': voting_result, 
            'weights': data['seat_weights'], 
            'veto_party_name': data['veto_party_name'], 
            'data_id': data['id']}
    

if __name__ == '__main__':
    if task_args.task_setting in ["rawlsianism", "utilitarianism"] and task_args.voting_threshold_setting != 'simple_majority':
        exit(0)

    # load task datas
    task_datas = load_json(f'datas/task_datas/{task_args.party_num}/{task_args.eval_topic}.json')

    # load model
    if 'gpt' in task_args.model_name or 'deepseek' in task_args.model_name or 'gemini' in task_args.model_name:
        llm_model = llm_tokenizer = None
    else:
        llm_tokenizer, llm_model = load_models(task_args)

    results = []
    scores = []

    for data in task_datas:
        result = run_task(data)
        results.append({'topic': task_args.eval_topic,
                        'model': task_args.model_name_or_path,
                        'model_name': task_args.model_name,
                        'party_num': task_args.party_num,
                        'task_setting': task_args.task_setting,
                        'voting_threshold_setting': task_args.voting_threshold_setting,
                        'responses': result['responses'],
                        'eval_scores': result['eval_scores'],
                        'is_pass_simple_veto': result['is_pass_simple_veto'],
                        'is_pass_veto': result['is_pass_veto'],
                        'is_pass_simple_majority': result['is_pass_simple_majority'],
                        'is_pass_2_3_majority': result['is_pass_2_3_majority'],
                        'voting_result': result['voting_result'],
                        'weights': result['weights'],
                        'veto_party_name': result['veto_party_name'],
                        'data_id': result['data_id']})

        if task_args.task_setting == 'seat_apportionment':
            if task_args.voting_threshold_setting == 'veto_power':
                scores.append(result['is_pass_veto'])
            elif task_args.voting_threshold_setting == 'simple_majority':
                scores.append(result['is_pass_simple_majority'])
            elif task_args.voting_threshold_setting == '2_3_majority':
                scores.append(result['is_pass_2_3_majority'])
            else:
                scores.append(result['voting_result'])
        else:
            scores.append(result['voting_result'])
    
    # save results
    if task_args.task_setting == 'seat_apportionment':
        save_json(results, f'results/eubench_logs/{task_args.party_num}/{task_args.eval_topic}/{task_args.voting_threshold_setting}/{task_args.model_name}.json')
        if task_args.voting_threshold_setting in ['veto_power', 'simple_majority', '2_3_majority']:
            print(f'Model: {task_args.model_name}; PartyNum: {task_args.party_num}; Topic: {task_args.eval_topic}\nSetting: {task_args.task_setting}-{task_args.voting_threshold_setting} result is {scores.count(1)/len(scores)}')
            rsts = {'model': task_args.model_name, 'party_num': task_args.party_num, 'task_args.party_num': task_args.party_num, 'topic': task_args.eval_topic, 'political_goal': task_args.voting_threshold_setting, 'result': scores.count(1)/len(scores)}
        else:
            print(f'Model: {task_args.model_name}; PartyNum: {task_args.party_num}; Topic: {task_args.eval_topic}\nSetting: {task_args.task_setting}-{task_args.voting_threshold_setting} result is {sum(scores)/len(scores)}')
            rsts = {'model': task_args.model_name, 'party_num': task_args.party_num, 'task_args.party_num': task_args.party_num, 'topic': task_args.eval_topic, 'political_goal': task_args.voting_threshold_setting, 'result': sum(scores)/len(scores)}
        save_json(rsts, f'results/eubench_rsts/{task_args.party_num}/{task_args.eval_topic}/{task_args.voting_threshold_setting}/{task_args.model_name}.json')
    else:
        save_json(results, f'results/eubench_logs/{task_args.party_num}/{task_args.eval_topic}/{task_args.task_setting}/{task_args.model_name}.json')
        print(f'Model: {task_args.model_name}; PartyNum: {task_args.party_num}; Topic: {task_args.eval_topic}\nSetting: {task_args.task_setting}-{task_args.voting_threshold_setting} result is {sum(scores)/len(scores)}')
        rsts = {'model': task_args.model_name, 'party_num': task_args.party_num, 'task_args.party_num': task_args.party_num, 'topic': task_args.eval_topic, 'political_goal': task_args.task_setting, 'result': sum(scores)/len(scores)}
    
        save_json(rsts, f'results/eubench_rsts/{task_args.party_num}/{task_args.eval_topic}/{task_args.task_setting}/{task_args.model_name}.json')

