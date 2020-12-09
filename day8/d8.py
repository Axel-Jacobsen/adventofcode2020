#! /usr/bin/env python3

from typing import Tuple, List, Set
from typing_extensions import Literal


OpCode = Literal["nop", "acc", "jmp"]


def evaluate(tape: List[Tuple[OpCode, int]]) -> int:
    idx: int = 0
    global_accumulator: int = 0
    seen_idxs: Set[int] = set()

    while True:
        if idx in seen_idxs:
            # infinite loop
            raise RuntimeError(
                f"IDX {idx} ALREADY EXECUTED; ACC = {global_accumulator}"
            )
        elif idx >= len(tape):
            # ran entire tape
            return global_accumulator
        seen_idxs.add(idx)

        op_code, v = tape[idx]
        if op_code == "nop":
            idx += 1
        elif op_code == "acc":
            global_accumulator += v
            idx += 1
        elif op_code == "jmp":
            idx += v


def swap_jmp_nops(tape: List[Tuple[OpCode, int]]) -> int:
    for i, (op_code, v) in enumerate(tape):
        try:
            if op_code == "jmp":
                tape[i] = ("nop", v)
            elif op_code == "nop" and v != 0:
                tape[i] = ("jmp", v)
            return evaluate(tape)
        except RuntimeError:
            pass
        finally:
            tape[i] = (op_code, v)
    raise RuntimeError("couldn't find a switch that worked")


with open("input.txt", "r") as f:
    tape: List[Tuple[OpCode, int]] = []
    for line in f.readlines():
        opcode, v = line.replace("+", "").split(" ")
        tape.append((opcode, int(v)))

    print(swap_jmp_nops(tape))
