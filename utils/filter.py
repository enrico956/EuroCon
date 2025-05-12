import re

def remove_intro_sentence(text):
    # Use regular expressions to match sentences starting with "Here" and ending with ":"
    pattern = r'^Here.*?:\s*'
    # Replace the matched part with an empty string
    return re.sub(pattern, '', text, count=1)

# # Example
# text = "Here is a revised answer that incorporates both opinions: This is the rest of the text."
# result = remove_intro_sentence(text)
# print(result)  # Output: "This is the rest of the text."


def rule_based_filter(responses):
    responses = remove_intro_sentence(responses)
    if responses.startswith("assistant\n\n"):
        responses = responses[len("assistant\n\n"):]
    if responses.startswith("\n\n"):
        responses = responses[len("\n\n"):]
    if responses.startswith("assistant "):
        responses = responses[len("assistant "):]
    if responses.startswith("assistant"):
        responses = responses[len("assistant"):]
    if responses.startswith(" "):
        responses = responses[len(" "):]
    responses = remove_intro_sentence(responses)
        
    return responses