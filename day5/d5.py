#! /usr/bin/env python3


def get_row_col(seat_bsp: str) -> int:
    row_bsp_ref = seat_bsp[:7].replace("F", "0").replace("B", "1")
    col_bsp_ref = seat_bsp[7:].replace("L", "0").replace("R", "1")
    return int(row_bsp_ref, 2), int(col_bsp_ref, 2)


with open("input.txt", "r") as f:
    seat_ids = sorted(
        8 * get_row_col(line.strip())[0] + get_row_col(line.strip())[1] for line in f.readlines()
    )
    print("part 1", seat_ids[-1])
    for s1, s2 in zip(seat_ids, seat_ids[1:]):
        if s2 - s1 == 2:
            print("part 2", s1 + 1)
            break
