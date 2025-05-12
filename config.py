import os
import argparse

import torch

parser = argparse.ArgumentParser(description='EuroCon')
parser.add_argument('--env_name', type=str, default='EuroCon',
                    help='name of the environment type')
parser.add_argument('--task_setting', type=str, default='seat_apportionment',
                    help='name of the task setting, in [seat_apportionment, rawlsianism, utilitarianism]')
parser.add_argument('--model_name_or_path', type=str, default='/share/nlp/kangyipeng/Qwen/Qwen2.5-32B-Instruct',
                    help='name of the tested LLM, in [' \
                    'deepseek-r1,' \
                    'gpt-4o,' \
                    'gemini-2.5-flash-preview,' \
                    'meta-llama/Llama-3.3-70B-Instruct' \
                    'Qwen/Qwen2.5-72B-Instruct,' \
                    'Qwen/Qwen2.5-32B-Instruct]'
                    )
parser.add_argument('--device', type=str, default='cuda:0',
                    help='use which gpu device')
parser.add_argument('--multi_gpu', action='store_true', default=False,
                    help='whether to use multiple GPUs')
parser.add_argument('--top_p', type=float, default=0.95,
                    help='confidence interval')   
parser.add_argument('--voting_threshold_setting', type=str, default='simple_majority',
                    help='name of the voting threshold setting, in [simple_majority, 2_3_majority, veto_power, none]')
parser.add_argument('--party_num', type=int, default=2,
                    help='number of the joined political groups, in [2, 4, 6]')
parser.add_argument('--eval_topic', type=str, default='gender equality',
                    help='name of the topic, in task_infos.py')
parser.add_argument('--max_new_tokens', type=int, default=512,
                    help='max generation new token num')
parser.add_argument('--temperature', type=float, default=0.7,
                    help='generation randomness')   
parser.add_argument('--seed', type=int, default=42,
                    help='randomnesss control')


args = parser.parse_args()

args.model_name = args.model_name_or_path.split('/')[-1]

args.device = torch.device(args.device if torch.cuda.is_available() else "cpu")

# print("=================Arguments==================")
# for k, v in args.__dict__.items():
#     print('{}: {}'.format(k, v))
# print("========================================")


