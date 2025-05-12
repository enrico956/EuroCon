def apply_template(tokenizer, sys_prompt, batch):
    batch_input = []
    # construct messages
    messages = [
        [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": batch[i]}
        ] for i in range(len(batch))
    ]
    for message in messages:
        message_text = tokenizer.apply_chat_template(message, tokenize=False, add_generation_prompt=False)
        batch_input.append(message_text)
    
    batch_inputs = tokenizer(batch_input, padding=True, truncation=True, add_special_tokens=True, max_length=4096, return_tensors="pt")
    return batch_inputs.input_ids

def apply_template_multi_sys(tokenizer, sys_prompts, batch):
    batch_input = []
    # construct messages
    messages = [
        [
            {"role": "system", "content": sys_prompts[i]},
            {"role": "user", "content": batch[i]}
        ] for i in range(len(batch))
    ]
    for message in messages:
        message_text = tokenizer.apply_chat_template(message, tokenize=False, add_generation_prompt=False)
        batch_input.append(message_text)
    
    batch_inputs = tokenizer(batch_input, padding=True, truncation=True, add_special_tokens=True, max_length=4096, return_tensors="pt")
    return batch_inputs.input_ids

def apply_template_multi(tokenizer, sys_prompt, prompt, batch_size):
    batch_input = []
    # construct messages
    messages = [
        [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ] for i in range(batch_size)
    ]
    for message in messages:
        message_text = tokenizer.apply_chat_template(message, tokenize=False, add_generation_prompt=False)
        batch_input.append(message_text)
    
    batch_inputs = tokenizer(batch_input, padding=True, truncation=True, add_special_tokens=True, max_length=4096, return_tensors="pt")
    return batch_inputs.input_ids


def apply_template_single(tokenizer, sys_prompt, prompt):
    # construct messages
    message = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": prompt}
    ]
    message_text = tokenizer.apply_chat_template(message, tokenize=False, add_generation_prompt=False)

    batch_input = tokenizer(message_text, padding=True, truncation=True, add_special_tokens=True, max_length=4096, return_tensors="pt")
    return batch_input.input_ids

def apply_template_mistral(tokenizer, sys_prompt, prompt, batch):
    batch_input = []
    # construct messages
    batch_input = [sys_prompt + " \n" + prompt for i in range(len(batch))]
    batch_inputs = tokenizer(batch_input, padding=True, truncation=True, add_special_tokens=True, max_length=4096, return_tensors="pt")
    return batch_inputs.input_ids