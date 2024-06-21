import re
import json

#====orignial code ======
# def read_jsonl(path: str):
#     with open(path) as fh:
#         return [json.loads(line) for line in fh.readlines() if line]

# ===== original code =====
# def gsm_extract_answer(completion):
#     match = re.search(r"(\-?[0-9\.\,]+)", completion)
#     return match.group(1).strip() if match else "[invalid]"


# def gsm_extract_answer(answer):
#     """Extract the answer from the GSM8k dataset format."""
#     match = re.search(r"#### (\-?[0-9\.\,]+)", answer)
#     return match.group(1).strip() if match else None

# === orginial code ======
# def check_answer_in_response(model_answer, expected_answer):
#     """Check if the expected answer is present in the model's response."""
#     return bool(re.search(re.escape(expected_answer), model_answer))



# ----- Second attempt working --------
# def check_answer_in_response(model_answer, expected_answer):
#   """Check if the expected answer is present in the model's response, handling missing answers."""
#   if not expected_answer:  # Check if expected_answer is None or empty string
#     return False  # Answer is missing, so not considered correct
#   try:
#     expected_answer = expected_answer.encode('utf-8').decode('latin-1')  # Encode and decode for handling non-latin characters
#     return bool(re.search(re.escape(expected_answer), model_answer))
#   except AttributeError:  # Handle potential issues during encoding/decoding
#     print(f"Error processing answer: {expected_answer}")  # Log the error for debugging
#     return False  # Consider the answer incorrect due to processing error


#===This working just try original now======
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







