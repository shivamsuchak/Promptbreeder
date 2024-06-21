import re
import json

def read_jsonl(path: str):
    """Reads a JSONL file and returns a list of dictionaries."""
    with open(path, 'r') as fh:
        return [json.loads(line) for line in fh.readlines() if line.strip()]

def gsm_extract_answer(completion: str) -> str:
    """Extracts the answer from the completion text."""
    return completion.strip()

def check_answer_in_response(model_answer: str, expected_answer: str) -> bool:
    """Check if the expected answer is present in the model's response."""
    # Normalize the answers to make the comparison more robust
    model_answer = model_answer.lower().strip()
    expected_answer = expected_answer.lower().strip()
    return expected_answer in model_answer







