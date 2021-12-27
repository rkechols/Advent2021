import os
import re
from typing import Dict, List

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


def get_variables() -> Dict[str, Variable]:
    return {letter: Variable(0) for letter in "wxyz"}


def evaluate(instruction: str, variables: Dict[str, Variable], next_digit_index: int, digits: List[int]) -> bool:
    if (inp_match := INP_RE.fullmatch(instruction)) is not None:
        receiver_var = inp_match.group(1)
        receiver_var = variables[receiver_var]
        receiver_var.value = digits[next_digit_index]
        return True
    else:
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
        return False


def validate(instructions: List[str], digits: List[int]) -> bool:
    variables = get_variables()
    next_digit_index = 0
    for instruction in instructions:
        if evaluate(instruction, variables, next_digit_index, digits):
            next_digit_index += 1
    valid = (variables["z"] == 0)
    return valid


def generate_options():
    digits = [9 for _ in range(N_DIGITS)]
    while True:
        for i in range(N_DIGITS - 1, -1, -1):
            if digits[i] != 1:
                digits[i] -= 1
                break  # yield then restart the while-loop
            else:  # rollover and move to the next digit
                digits[i] = 9
        else:  # all the digits were 1; end of generation
            break  # exit the while-loop
        yield digits


if __name__ == "__main__":
    instructions_ = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            instructions_.append(line_.strip())
    # part 1
    number = None
    for digits_ in generate_options():
        valid_ = validate(instructions_, digits_)
        if valid_:
            number = "".join(str(d) for d in digits_)
            break
    else:
        raise ValueError("No valid number?")
    print(f"HIGHEST valid number: {number}")
