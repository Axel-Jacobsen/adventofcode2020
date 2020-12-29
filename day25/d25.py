#! /usr/bin/env python3


test_card_key = 5764801
test_door_key = 17807724

card_key = 11239946
door_key = 10464955


def transform(sn, loop_size):
    dv = 20201227
    p = 1
    for _ in range(loop_size):
        p = p * sn % dv
    return p


def get_loop_key(pubkey):
    dv = 20201227
    i, p = 0, 1
    while True:
        i += 1
        p = p * 7 % dv
        if p == pubkey:
            return i


def p1(ck, dk):
    card_loop_num = get_loop_key(ck)
    door_loop_num = get_loop_key(dk)
    print(card_loop_num, door_loop_num)
    return transform(ck, door_loop_num)

print(p1(card_key, door_key))
