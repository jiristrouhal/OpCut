import re


VALID_RAW_PIECE_PATTERN = "\( *[123456789][0123456789]* *, *[123456789][0123456789]* *\)"


def is_raw_valid(tested_input:str)->bool:
    items = tested_input.split(";")

    for item in items: 
        item=item.strip()
        if item=="": continue
        if not raw_complies_with_pattern(item): return False
    return True


def raw_complies_with_pattern(tested_item:str):
    if re.fullmatch(VALID_RAW_PIECE_PATTERN, tested_item) is None: return False
    return True
