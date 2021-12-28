import os
import re
from typing import Dict, List, Tuple

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input24.txt")

INP_RE = re.compile(r"inp ([wxyz])")
BINARY_OP_RE = re.compile(r"(add|mul|div|mod|eql) ([wxyz]) ([wxyz]|-?\d+)")

N_DIGITS = 14

VAR_TO_INDEX = {char: i_ for i_, char in enumerate("wxyz")}
OP_TO_FUNCTION = {
    "add": lambda x, y: x + y,
    "mul": lambda x, y: x * y,
    "div": lambda x, y: int(x / y),
    "mod": lambda x, y: int(x % y),
    "eql": lambda x, y: int(x == y)
}


def evaluate(instruction: str, variables: Dict[Tuple[int, ...], str]) -> Dict[Tuple[int, ...], str]:
    match = BINARY_OP_RE.fullmatch(instruction)
    command, receiver_var, val = match.groups()
    func = OP_TO_FUNCTION[command]
    receiver_var_index = VAR_TO_INDEX[receiver_var]
    new_variables = dict()
    for var_tup, value_s in variables.items():
        try:
            val = int(val)
        except ValueError:
            val = var_tup[VAR_TO_INDEX[val]]
        var_list = list(var_tup)
        var_list[receiver_var_index] = func(var_tup[receiver_var_index], val)
        new_variables[tuple(var_list)] = value_s
    return new_variables


def solve_greatest(instructions: List[str]) -> int:
    variables = {(0, 0, 0, 0): ""}
    for instruction in instructions:
        if (match := INP_RE.fullmatch(instruction)) is not None:
            # input command gets special treatment
            receiver_var = match.group(1)
            receiver_var_index = VAR_TO_INDEX[receiver_var]
            new_variables = dict()
            for var_tup, value_s in variables.items():
                for i in range(1, 10):  # branch out
                    var_list = list(var_tup)
                    var_list[receiver_var_index] = i
                    new_tup = tuple(var_list)
                    new_value_s = f"{value_s}{i}"
                    if new_tup in new_variables:
                        # which is bigger?
                        new_value = int(new_value_s)
                        if new_value > int(new_variables[new_tup]):
                            new_variables[new_tup] = new_value_s
                    else:
                        new_variables[new_tup] = new_value_s
            variables = new_variables
        else:  # just execute the command
            variables = evaluate(instruction, variables)
    # find the biggest with a 0 for z
    z_index = VAR_TO_INDEX["z"]
    biggest = None
    for var_tup, value_s in variables.items():
        if var_tup[z_index] == 0:
            value = int(value_s)
            if biggest is None or value > biggest:
                biggest = value
    return biggest


if __name__ == "__main__":
    instructions_ = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            instructions_.append(line_.strip())
    # part 1
    number = solve_greatest(instructions_)
    print(f"HIGHEST valid number: {number}")