import re

def strip_code_block_fence(text: str):
    cleaned = re.sub(r"```(?:python)?", "", text)
    cleaned = cleaned.replace("```", "").strip()

    return cleaned

def fix_invalid_json_backslashes(text: str) -> str:
    json_str = re.sub(r'(?<!\\)\\(?![\\nt"\/])', r'\\\\', text)
    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)

    return json_str