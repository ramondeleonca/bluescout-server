import re

def parse_csv_to_dict(csv_str: str):
    lines = csv_str.split('\n')
    keys = re.split(r"(?<!\\),", lines[0])
    values = re.split(r"(?<!\\),", lines[1])
    
    return dict(zip(keys, values))