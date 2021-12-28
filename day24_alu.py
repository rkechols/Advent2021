import os
import re
from typing import Dict, List, Tuple

from constants import INPUTS_DIR, UTF_8
from tqdm import tqdm


INPUT_FILE = os.path.join(INPUTS_DIR, "input24.txt")

INP_RE = re.compile(r"inp ([wxyz])")
BINARY_OP_RE = re.compile(r"(add|mul|div|mod|eql) ([wxyz]) ([wxyz]|-?\d+)")

N_DIGITS = 14

VAR_TO_INDEX = {char: i_ for i_, char in enumerate("wxyz")}
OP_TO_FUNCTION = {
    "add": lambda a, b: a + b,
    "mul": lambda a, b: a * b,
    "div": lambda a, b: int(a / b),
    "mod": lambda a, b: int(a % b),
    "eql": lambda a, b: int(a == b)
}


def evaluate(instruction: str, variables: Dict[Tuple[int, ...], str]) -> Dict[Tuple[int, ...], str]:
    # evaluate this single instruction
    match = BINARY_OP_RE.fullmatch(instruction)
    command, receiver_var, val_s = match.groups()
    func = OP_TO_FUNCTION[command]
    receiver_var_index = VAR_TO_INDEX[receiver_var]
    new_variables = dict()
    for var_tup, value_s in variables.items():
        try:
            val = int(val_s)
        except ValueError:
            val = var_tup[VAR_TO_INDEX[val_s]]
        var_list = list(var_tup)
        var_list[receiver_var_index] = func(var_tup[receiver_var_index], val)
        new_variables[tuple(var_list)] = value_s
    return new_variables


def solve_greatest(instructions: List[str]) -> int:
    variables = {(0, 0, 0, 0): ""}
    with tqdm(total=len(instructions)) as progress:
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
            # update the progress bar
            progress.set_description(f"# of states = {len(variables)}")
            progress.update()
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
