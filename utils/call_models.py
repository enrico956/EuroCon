import re
import os
import sys
import time

import torch
from openai import OpenAI

from openai_keys import OPENAI_API_KEY, OPENAI_BASE_URL
from utils.apply_template import apply_template_single

def gen_model_responses(model, tokenizer, args, sysprompt = "You are a helpful assistant.", prompt = ''):
    if model is None or tokenizer is None:
        try:
            if 'gpt-4o' in args.model_name:
                completion = OpenAI(api_key = OPENAI_API_KEY, base_url = OPENAI_BASE_URL).chat.completions.create(
                                    model = "gpt-4o-2024-08-06", 
                                    messages = [
                                        {"role": "system", "content": sysprompt},
                                        {"role": "user", "content": f"{prompt}"}
                                    ],
                                    max_tokens = args.max_new_tokens,
                                    temperature = args.temperature,
                                    top_p = args.top_p,
                                    seed = args.seed 
                                )
                return completion.choices[0].message.content
            elif 'deepseek-r1' in args.model_name:
                completion = OpenAI(api_key = OPENAI_API_KEY, base_url = OPENAI_BASE_URL).chat.completions.create(
                                    model = "deepseek-r1-250120", 
                                    messages = [
                                        {"role": "system", "content": sysprompt},
                                        {"role": "user", "content": f"{prompt}"}
                                    ],
                                    max_tokens = args.max_new_tokens,
                                    temperature = args.temperature,
                                    top_p = args.top_p,
                                    seed = args.seed 
                                )
                return completion.choices[0].message.content
            elif 'gemini' in args.model_name:
                completion = OpenAI(api_key = OPENAI_API_KEY, base_url = OPENAI_BASE_URL).chat.completions.create(
                                    model = "gemini-2.5-flash-preview-04-17-thinking", 
                                    messages = [
                                        {"role": "system", "content": sysprompt},
                                        {"role": "user", "content": f"{prompt}"}
                                    ],
                                    max_tokens = args.max_new_tokens,
                                    temperature = args.temperature,
                                    top_p = args.top_p,
                                    seed = args.seed 
                                )
            else:
                raise ValueError(f"Model {args.model_name} not supported.")
            
        except Exception as e:
            print(e, file=sys.stderr)
            time.sleep(10)
    
    else: # use opensource model to generate responses
        input_ids = apply_template_single(tokenizer, sysprompt, prompt).to(model.device)
        init_len = input_ids.shape[-1]

        with torch.no_grad():
            outputs = model.generate(
                input_ids = input_ids,
                pad_token_id = tokenizer.eos_token_id,
                max_new_tokens = args.max_new_tokens,
                do_sample = False,
                temperature = args.temperature,
                top_p = args.top_p,
            )
        responses = tokenizer.decode(outputs[:, init_len:].squeeze(), skip_special_tokens=True) 
        
        return responses
        