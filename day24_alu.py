import os
import re
from typing import Dict, List, Optional
from copy import copy, deepcopy

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input24.txt")

INP_RE = re.compile(r"inp ([wxyz])")
BINARY_OP_RE = re.compile(r"(add|mul|div|mod|eql) ([wxyz]) ([wxyz]|-?\d+)")

INPUT = "inp"
ADD = "add"
MUL = "mul"
DIV = "div"
MOD = "mod"
EQL = "eql"

N_DIGITS = 14


class Variable:
    def __init__(self, value: int):
        self.value = value

    def __repr__(self) -> str:
        return f"Variable({self.value})"


def get_variables() -> Dict[str, Variable]:
    return {letter: Variable(0) for letter in "wxyz"}


def evaluate(instruction: str, variables: Dict[str, Variable]):
    match = BINARY_OP_RE.fullmatch(instruction)
    command, receiver_var, val = match.groups()
    receiver_var = variables[receiver_var]
    try:
        val = int(val)
    except ValueError:
        val = variables[val].value
    if command == ADD:
        receiver_var.value += val
    elif command == MUL:
        receiver_var.value *= val
    elif command == DIV:
        receiver_var.value = int(receiver_var.value / val)
    elif command == MOD:
        receiver_var.value = int(receiver_var.value % val)
    elif command == EQL:
        receiver_var.value = int(receiver_var.value == val)
    else:
        raise ValueError(f"invalid command: \"{instruction}\"")


def validate_dfs(variables: Dict[str, Variable], instructions: List[str], instruction_index: int = 0, digits: List[int] = None) -> Optional[List[int]]:
    if digits is None:
        digits = list()
    n = len(instructions)
    while instruction_index < n:
        instruction = instructions[instruction_index]
        instruction_index += 1
        if (inp_match := INP_RE.fullmatch(instruction)) is not None:
            receiver_var_name = inp_match.group(1)
            for digit in range(9, 0, -1):
                new_vars = deepcopy(variables)
                receiver_var = new_vars[receiver_var_name]
                receiver_var.value = digit
                new_digits = copy(digits)
                new_digits.append(digit)
                answer = validate_dfs(new_vars, instructions, instruction_index, new_digits)
                if answer is not None:
                    return answer
        else:
            evaluate(instruction, variables)
    if variables["z"] == 0:
        return digits
    else:
        return None


if __name__ == "__main__":
    instructions_ = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            instructions_.append(line_.strip())
    # part 1
    variables_ = get_variables()
    answer_ = validate_dfs(variables_, instructions_)
    number = "".join(str(d) for d in answer_)
    print(f"HIGHEST valid number: {number}")
