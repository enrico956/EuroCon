import re
import os
import sys
import time

import torch
from openai import OpenAI

from openai_keys import OPENAI_API_KEY, OPENAI_BASE_URL


def gen_chatgpt_outputs(sysprompt = "You are a helpful assistant.", prompt = '', max_token = 200, temperature = 0.0, top_p = 0.95, seed = 42):       
    while True:
        try:
            completion = OpenAI(api_key = OPENAI_API_KEY, base_url = OPENAI_BASE_URL).chat.completions.create(
                                    model = "gpt-4o-mini-2024-07-18", 
                                    messages = [
                                        {"role": "system", "content": sysprompt},
                                        {"role": "user", "content": f"{prompt}"}
                                    ],
                                    max_tokens = max_token,
                                    temperature = temperature,
                                    top_p = top_p,
                                    seed = seed 
                                )
            return completion.choices[0].message.content
            
        except Exception as e:
            print(e, file=sys.stderr)
            time.sleep(5)
            
    
