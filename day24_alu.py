import os
import re
from typing import Dict, List, Tuple
from functools import lru_cache
from constants import INPUTS_DIR, UTF_8
from tqdm import tqdm


INPUT_FILE = os.path.join(INPUTS_DIR, "input24.txt")

INP_RE = re.compile(r"inp ([wxyz])")
REDUNDANT_BINARY_OP_RE = re.compile(r"add [wxyz] 0|mul [wxyz] 1|div [wxyz] 1")
BINARY_OP_RE = re.compile(r"(add|mul|div|mod|eql) ([wxyz]) ([wxyz]|-?\d+)")

N_DIGITS = 14

VAR_TO_INDEX = {char: i_ for i_, char in enumerate("wxyz")}


@lru_cache
def add(a, b):
    return a + b


@lru_cache
def mul(a, b):
    return a * b


@lru_cache
def div(a, b):
    return int(a / b)


@lru_cache
def mod(a, b):
    return a % b


@lru_cache
def eql(a, b):
    return int(a == b)


OP_TO_FUNCTION = {
    "add": add,
    "mul": mul,
    "div": div,
    "mod": mod,
    "eql": eql
}


def evaluate(instruction: str, variables: Dict[Tuple[int, ...], str]) -> Dict[Tuple[int, ...], str]:
    if REDUNDANT_BINARY_OP_RE.fullmatch(instruction) is not None:
        # useless command: don't do anything
        return variables
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
    n = len(instructions_)
    # delay "inp" commands until they're actually relevant
    i_ = 0
    while i_ < n - 1:
        this_instruction = instructions_[i_]
        if (inp_match_ := INP_RE.fullmatch(this_instruction)) is not None:
            inp_var = inp_match_.group(1)
            while i_ < n - 1:
                next_instruction = instructions_[i_ + 1]
                if re.search(rf"\b{inp_var}\b", next_instruction) is not None:
                    break
                instructions_[i_ + 1] = this_instruction
                instructions_[i_] = next_instruction
                i_ += 1
        i_ += 1
    # part 1
    number = solve_greatest(instructions_)
    print(f"HIGHEST valid number: {number}")
