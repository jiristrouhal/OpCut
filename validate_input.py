import re


def is_raw_valid(tested_input:str)->bool:
    if tested_input.strip()=="": return True

    if tested_input.count(")")!=tested_input.count("("): return False

    if re.fullmatch("\( *\)", tested_input): return False

    return True