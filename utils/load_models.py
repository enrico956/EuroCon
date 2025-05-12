import os

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def load_models(args):

    print('cuda device_count:', torch.cuda.device_count())
    print('cuda is_available:', torch.cuda.is_available())

    model_name = args.model_name_or_path

    llm_tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if llm_tokenizer.pad_token is None:
        llm_tokenizer.pad_token = llm_tokenizer.eos_token

   if args.multi_gpu:
        llm_model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype = torch.bfloat16, device_map = 'auto'
        )
    else:
        llm_model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype = torch.bfloat16
        )

    if args.multi_gpu:
        llm_model = llm_model.eval()
    else:
        llm_model = llm_model.eval().to(args.device)

    return llm_tokenizer, llm_model

